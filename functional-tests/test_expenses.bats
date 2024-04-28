#!/usr/bin/env bats

# per whole file
setup_file() {
    curdir="${BATS_TEST_FILENAME%/*}"
    db_host="127.0.0.1"
    test_db="expenses"
    test_db_pass="dummypass"
    test_db_user="expenses"
    mysql="mysql \
        --host=$db_host \
        --port=3306 \
        --protocol=tcp \
        --user=$test_db_user \
        --password=$test_db_pass"

    $mysql -e "drop database if exists $test_db"
    $mysql -e "create database $test_db"
    $mysql "$test_db" < $curdir/../db/schema.sql
    $mysql -e "insert into accounts values (0, 'Test account 0'),(1, 'Test account 1')" "$test_db"
    $mysql -e "select * from expenses;" "$test_db"
}


# per test
setup() {
    load helpers
}

@test "I can get the expenses (empty database)" {
    run do_get "api/expenses"

    [[ "$status" == "0" ]]
    is_equal \
        '[]' \
        "$output"
}

@test "I can create a new expense" {
    new_expense='{
        "currency": "EUR",
        "amount": "42.0",
        "category": "eating-out",
        "description": "Some fake expense number 1",
        "accountId": 1,
        "timestamp": "'"$(date +%Y-%m-%dT%H:%M:%SZ)"'"
    }'
    run do_post "api/expenses" "$new_expense"

    [[ "$status" == "0" ]]
    json_has_match 'amount' '42' "$output"
    json_has_match 'category' 'eating-out' "$output"
    json_has_match 'description' 'Some fake expense number 1' "$output"
    json_has_match 'account.id' '1' "$output"
}

@test "I can update an expense" {
    new_expense='{
        "currency": "EUR",
        "amount": "42.0",
        "category": "eating-out",
        "description": "Some fake expense number 1",
        "accountId": 1,
        "timestamp": "'"$(date +%Y-%m-%dT%H:%M:%SZ)"'"
    }'
    run do_post "api/expenses" "$new_expense"

    [[ "$status" == "0" ]]
    json_has_match 'amount' '42' "$output"

    new_expense_id="$(echo "$output" | json_get "id")"
    modified_expense='{
        "currency": "EUR",
        "amount": "84.0",
        "category": "eating-out",
        "description": "Some fake expense number 1",
        "accountId": 1,
        "timestamp": "'"$(date +%Y-%m-%dT%H:%M:%SZ)"'"
    }'
    run do_put "api/expenses/$new_expense_id" "$modified_expense"

    [[ "$status" == "0" ]]
    json_has_match "amount" '84' "$output"

    run do_get "api/expenses"

    json_has_match "[] | select( .id == $new_expense_id) | .amount" '84' "$output"
}

@test "I can delete an expense" {
    new_expense='{
        "currency": "EUR",
        "amount": "42.0",
        "category": "eating-out",
        "description": "Some fake expense number 1",
        "accountId": 1,
        "timestamp": "'"$(date +%Y-%m-%dT%H:%M:%SZ)"'"
    }'
    run do_post "api/expenses" "$new_expense"

    [[ "$status" == "0" ]]
    json_has_match 'amount' '42' "$output"

    new_expense_id="$(echo "$output" | json_get "id")"

    run do_delete "api/expenses/$new_expense_id"

    [[ "$status" == "0" ]]
    [[ "$output" == "$new_expense_id" ]]

    run do_get "api/expenses"

    json_has_match "[] | select( .id == $new_expense_id)" '' "$output"
}
