"""Watchdog for the explicit corpus, latency and concurrency benchmark modules."""
import argparse
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

from tests.performance.phase17h import configuration, inventory, write


def run(module, output, config):
    if module not in ('corpus','latency','workloads'):raise ValueError('unknown suite')
    output=output.resolve()
    if output.exists() or output.is_relative_to(Path.cwd().resolve()):
        raise ValueError('new outside-repository directory required')
    output.mkdir(parents=True)
    start=time.monotonic();peak_rss=peak_bytes=peak_files=0;reason=None
    with (output/'child.log').open('w') as log:
        process=subprocess.Popen([sys.executable,'-m',f'tests.performance.{module}','--output',str(output/'run')],
            stdout=log,stderr=log,env={**os.environ,'OPENBLAS_NUM_THREADS':'1','OMP_NUM_THREADS':'1','MKL_NUM_THREADS':'1'})
        try:
            while process.poll() is None:
                stats=inventory(output)
                peak_bytes=max(peak_bytes,stats['bytes']);peak_files=max(peak_files,stats['files'])
                try:rss=int(Path(f'/proc/{process.pid}/statm').read_text().split()[1])*os.sysconf('SC_PAGE_SIZE')
                except (FileNotFoundError,ProcessLookupError):rss=0
                peak_rss=max(peak_rss,rss)
                if time.monotonic()-start>config['max_seconds']:reason='wall_budget'
                if rss>config['max_address_bytes']:reason='rss_budget'
                if stats['bytes']>config['max_disk_bytes']:reason='disk_budget'
                if stats['files']>config['max_files']:reason='file_budget'
                if reason:process.kill();break
                time.sleep(.2)
            process.wait(timeout=10)
        finally:
            if process.poll() is None:process.kill();process.wait(timeout=10)
    result={'module':module,'elapsed_seconds':time.monotonic()-start,'exit_code':process.returncode,
        'stop_reason':reason,'sampled_peak_rss_bytes':peak_rss,'sampled_peak_disk_bytes':peak_bytes,
        'sampled_peak_files':peak_files,'sampling_seconds':.2,'limits':config,
        'python':platform.python_version(),'platform':platform.platform(),'cpu_count':os.cpu_count(),
        'status':'PASS' if not reason and process.returncode==0 else 'FAIL'}
    write(output/'resource.json',result)
    return result


if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--module',choices=('corpus','latency','workloads'),required=True)
    p.add_argument('--output',type=Path,required=True)
    p.add_argument('--config',type=Path,default=Path('tests/fixtures/phase17h/profile.json'))
    args=p.parse_args();result=run(args.module,args.output,configuration(args.config))
    print(result['status'],result['elapsed_seconds'])
    raise SystemExit(0 if result['status']=='PASS' else 1)
