# Ohtaigi Slides

## Prerequisites
1. Add password to Google Cloud Secret Manager
2. Allow service account to access the password

## Deployment
1. `gcloud builds submit --tag gcr.io/{PROJECT_ID}/ohtaigi-slides`
2. `gcloud run deploy --image gcr.io/{PROJECT_ID}/ohtaigi-slides --platform managed`