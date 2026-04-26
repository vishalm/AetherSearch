{{/*
Expand the name of the chart.
*/}}
{{- define "aethersearch.name" -}}
{{- default .Chart.Name .Values.nameOverride | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Create a default fully qualified app name.
We truncate at 63 chars because some Kubernetes name fields are limited to this (by the DNS naming spec).
If release name contains chart name it will be used as a full name.
*/}}
{{- define "aethersearch.fullname" -}}
{{- if .Values.fullnameOverride }}
{{- .Values.fullnameOverride | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- $name := default .Chart.Name .Values.nameOverride }}
{{- if contains $name .Release.Name }}
{{- .Release.Name | trunc 63 | trimSuffix "-" }}
{{- else }}
{{- printf "%s-%s" .Release.Name $name | trunc 63 | trimSuffix "-" }}
{{- end }}
{{- end }}
{{- end }}

{{/*
Create chart name and version as used by the chart label.
*/}}
{{- define "aethersearch.chart" -}}
{{- printf "%s-%s" .Chart.Name .Chart.Version | replace "+" "_" | trunc 63 | trimSuffix "-" }}
{{- end }}

{{/*
Common labels
*/}}
{{- define "aethersearch.labels" -}}
helm.sh/chart: {{ include "aethersearch.chart" . }}
{{ include "aethersearch.selectorLabels" . }}
{{- if .Chart.AppVersion }}
app.kubernetes.io/version: {{ .Chart.AppVersion | quote }}
{{- end }}
app.kubernetes.io/managed-by: {{ .Release.Service }}
{{- end }}

{{/*
Selector labels
*/}}
{{- define "aethersearch.selectorLabels" -}}
app.kubernetes.io/name: {{ include "aethersearch.name" . }}
app.kubernetes.io/instance: {{ .Release.Name }}
{{- end }}

{{/*
Create the name of the service account to use
*/}}
{{- define "aethersearch.serviceAccountName" -}}
{{- if .Values.serviceAccount.create }}
{{- default (include "aethersearch.fullname" .) .Values.serviceAccount.name }}
{{- else }}
{{- default "default" .Values.serviceAccount.name }}
{{- end }}
{{- end }}

{{/*
Set secret name
*/}}
{{- define "aethersearch.secretName" -}}
{{- default .secretName .existingSecret }}
{{- end }}

{{/*
Create env vars from secrets
*/}}
{{- define "aethersearch.envSecrets" -}}
    {{- range $secretSuffix, $secretContent := .Values.auth }}
    {{- if and (ne $secretContent.enabled false) ($secretContent.secretKeys) }}
    {{- range $name, $key := $secretContent.secretKeys }}
- name: {{ $name | upper | replace "-" "_" | quote }}
  valueFrom:
    secretKeyRef:
      name: {{ include "aethersearch.secretName" $secretContent }}
      key: {{ default $name $key }}
    {{- end }}
    {{- end }}
    {{- end }}
{{- end }}

{{/*
Helpers for mounting a psql convenience script into pods.
*/}}
{{- define "aethersearch.pgInto.enabled" -}}
{{- if and .Values.tooling .Values.tooling.pgInto .Values.tooling.pgInto.enabled }}true{{- end }}
{{- end }}

{{- define "aethersearch.pgInto.configMapName" -}}
{{- printf "%s-pginto" (include "aethersearch.fullname" .) -}}
{{- end }}

{{- define "aethersearch.pgInto.checksumAnnotation" -}}
{{- if (include "aethersearch.pgInto.enabled" .) }}
checksum/pginto: {{ include (print $.Template.BasePath "/tooling-pginto-configmap.yaml") . | sha256sum }}
{{- end }}
{{- end }}

{{- define "aethersearch.pgInto.volumeMount" -}}
{{- if (include "aethersearch.pgInto.enabled" .) }}
- name: pginto-script
  mountPath: {{ default "/usr/local/bin/pginto" .Values.tooling.pgInto.mountPath }}
  subPath: pginto
  readOnly: true
{{- end }}
{{- end }}

{{- define "aethersearch.pgInto.volume" -}}
{{- if (include "aethersearch.pgInto.enabled" .) }}
- name: pginto-script
  configMap:
    name: {{ include "aethersearch.pgInto.configMapName" . }}
    defaultMode: 0755
{{- end }}
{{- end }}

{{- define "aethersearch.renderVolumeMounts" -}}
{{- $pginto := include "aethersearch.pgInto.volumeMount" .ctx -}}
{{- $existing := .volumeMounts -}}
{{- if or $pginto $existing -}}
volumeMounts:
{{- if $pginto }}
{{ $pginto | nindent 2 }}
{{- end }}
{{- if $existing }}
{{ toYaml $existing | nindent 2 }}
{{- end }}
{{- end -}}
{{- end }}

{{- define "aethersearch.renderVolumes" -}}
{{- $pginto := include "aethersearch.pgInto.volume" .ctx -}}
{{- $existing := .volumes -}}
{{- if or $pginto $existing -}}
volumes:
{{- if $pginto }}
{{ $pginto | nindent 2 }}
{{- end }}
{{- if $existing }}
{{ toYaml $existing | nindent 2 }}
{{- end }}
{{- end -}}
{{- end }}

{{/*
Return the configured autoscaling engine; defaults to HPA when unset.
*/}}
{{- define "aethersearch.autoscaling.engine" -}}
{{- $engine := default "hpa" .Values.autoscaling.engine -}}
{{- $engine | lower -}}
{{- end }}
