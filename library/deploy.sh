#!/bin/bash

source $1

v_war=$war
msg="Deployed OK"

curl --upload-file $v_war "http://arsen:arsen@127.0.0.1:8080/manager/text/deploy?path=/myapp&update=true"
echo "{\"changed\": true, \"msg\": \"$msg\", \"file\": \"$v_war\"}"

exit 0