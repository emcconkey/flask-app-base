#!/bin/bash

# Check the number of arguments
if [ $# -ne 4 ]; then
    echo "Usage: $0 <first> <last> <email> <password>"
    exit 1
fi

first=$1
last=$2
email=$3
password=$4

# Run flask shell and pass in the username and password
# Make sure this is run from the app/ directory
flask shell <<EOF
from app import db
from lib.user import User
user = User()
user.email = '$email'
user.first_name = '$first'
user.last_name = '$last'
user.set_password('$password')
user.admin_level = 2
user.status = 'active'
db.session.add(user)
db.session.commit()
print('User created successfully')
EOF

