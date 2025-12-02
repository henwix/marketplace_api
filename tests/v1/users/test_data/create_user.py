CREATE_USER_ARGNAMES = [
    'expected_first_name',
    'expected_last_name',
    'expected_email',
    'expected_phone',
    'expected_password',
]


CREATE_USER_ARGVALUES = [
    ('Hello', 'World', 'test@example.com', '+978658358284', 'test_password_123456'),
    ('John', 'Doe', 'john@example.com', '+18482612425', 'johndoe82461942'),
    ('Jane', 'Doe', 'JaneDoe@test.com', '+1234567690249238', 'JANE_DOE_PASSWORD-1029!@)$&0217501231'),
    ('Name', 'Test', 'HelloWorld@test.test', '+887674726472112', 'helloworld_1234+_()*#@!@(&$%)(*!@&^%!^$%(@!($)'),
]


CREATE_USER_WITH_NONE_ARGVALUES = [
    (None, 'World', 'test@example.com', '+978658358284', 'test_password_123456'),
    ('John', None, 'john@example.com', '+18482612425', 'johndoe82461942'),
    ('Jane', 'Doe', None, '+1234567690249238', 'JANE_DOE_PASSWORD-1029!@)$&0217501231'),
    ('Name', 'Test', 'HelloWorld@test.test', None, 'helloworld_1234+_()*#@!@(&$%)(*!@&^%!^$%(@!($)'),
]
