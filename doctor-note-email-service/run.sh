#!/bin/bash

cd googleAPI/google
deactivate
source myenv/bin/activate
python3 Google.py
cd ../../
deactivate
cd doctorNotes
source myenv/bin/activate
python3 email_parser.py
deactivate
cd ../../patient-review-email-service
source myenv/bin/activate
python3 reviews.py
deactivate
cd ../patient-followUp-email-service
python3 followUp.py

