#!/bin/bash

# Check the number of arguments
if [ $# -ne 2 ]; then
    echo "Usage: $0 <email> <password>"
    exit 1
fi

email=$1
password=$2

# Run flask shell and pass in the username and password
# Make sure this is run from the app/ directory
flask shell <<EOF
from app import db
from lib.user import User
user = User.query.filter_by(email='$email').first()
if not user:
    print('User not found')
    exit(1)

user.set_password('$password')
db.session.add(user)
db.session.commit()
print('Password reset successfully')
EOF

