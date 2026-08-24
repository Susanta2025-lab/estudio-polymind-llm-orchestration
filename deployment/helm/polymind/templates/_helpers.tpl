{{- define "polymind.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "polymind.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name (include "polymind.name" .) | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}

{{- define "polymind.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{- define "polymind.labels" -}}
helm.sh/chart: {{ include "polymind.chart" . }}
{{ include "polymind.selectorLabels" . }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}

{{- define "polymind.selectorLabels" -}}
app.kubernetes.io/name: {{ include "polymind.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{- define "polymind.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "polymind.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{- define "polymind.secretName" -}}
{{- if .Values.secrets.create }}{{ include "polymind.fullname" . }}{{ else }}{{ required "secrets.existingSecret is required when secrets.create=false" .Values.secrets.existingSecret }}{{ end }}
{{- end }}

