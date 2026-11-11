import os

SECRET_KEY = os.environ.get(
    "AQUAVERDE_SECRET_KEY",
    "grasomateoamilcaraquaverde"
)

ADMIN_USER = "admin"

# Pegaremos aquí el hash de la contraseña en el siguiente paso.
ADMIN_PASSWORD_HASH = "scrypt:32768:8:1$G9ImUY0SDUdmsGaB$59eb899489d6ede378d22d15c938f54fb33ffe6ccda95c48dcdbc1e536b09c0b89c9a4a6a7cc265c9ad2e2092cf3eb7b19208e4df7c2550130571f3d496a835f"
