#!/usr/bin/env bats
BASE_URL=http://127.0.0.1:8080

do_post() {
    local path="${1?}"
    local data="${2?}"
    curl \
        -X POST \
        --silent \
        "${BASE_URL}/${path}" \
        -H 'Content-Type: application/json' \
        -d "$data"
}

do_put() {
    local path="${1?}"
    local data="${2?}"
    curl \
        -X PUT \
        --silent \
        "${BASE_URL}/${path}" \
        -H 'Content-Type: application/json' \
        -d "$data"
}

do_get() {
    local path="${1?}"
    curl \
        -X GET \
        --silent \
        "${BASE_URL}/${path}" \
        -H 'Content-Type: application/json'
}

do_delete() {
    local path="${1?}"
    curl \
        -X DELETE \
        --silent \
        "${BASE_URL}/${path}" \
        -H 'Content-Type: application/json'
}

is_equal() {
    local left="${1?}"
    local right="${2?}"
    diff <( printf '%s' "$left" ) <( printf "%s" "$right" ) \
    && return 0
    echo -e "is_equal failed\nleft: $left\nright: $right" >&2
    return 1
}

match_regex() {
    local regex="${1?}"
    local what="${2?}"
    [[ "$what" =~ $regex ]] && return 0
    echo -e "match_regex failed\nregex: '$regex'\nwhat: $what" >&2
    return 1
}

json_has_equal() {
    local key="${1?}"
    local value="${2?}"
    local data="${3?}"
    local cur_value=$(echo "$data" | jq -r ".$key") \
    && is_equal "$cur_value" "$value" \
    && return 0
    echo -e "json_has_equal: key '$key' with value '$value' not found in \n$data" >&2
    return 1
}

json_has_match() {
    local key="${1?}"
    local match="${2?}"
    local data="${3?}"
    local cur_value=$(echo "$data" | jq -r ".$key")
    match_regex "$match" "$cur_value" && return 0
    echo -e "json_has_match: key '$key' value '$cur_value' does not match '$match'" >&2
    return 1
}

json_get() {
    local key="${1?}"
    jq -r ".$key"
}
