def test_courses_route(client, auth):
    with client:
        response = client.get('/courses')
        assert response.headers['Location'] == 'http://localhost/'

    with client:
        auth.login()
        response = client.get('/courses')
        assert 200 == response.status_code
        assert b'<h1>Courses</h1>' in response.data
        assert b"<form method='POST'>" in response.data
        assert b'<li><a href="/courses/1">CSET 155</a></li>' in response.data

    # extra thing which checks what happens when a student tries to enter
    with client:
        auth.login('student@stevenscollege.edu', 'asdfgh')
        response = client.get('/courses')
        # test that student got redirected home
        assert b'You are not permitted to view this page' in response.data


def test_create_course_validation(client, auth):
    with client:
        auth.login()
        response = client.post('/courses', data={
            'course': 'h',
            'course_number': '',
            'info': 'h',
        })
        assert b'<p>Course Number and Course fields required</p>' in response.data


def test_course_update_route(client, auth):
    with client:
        auth.login()
        response = client.get('/courses/1')
        assert 200 == response.status_code
        assert b'<h1>Update CSET 155</h1>' in response.data
        assert b"<form method='POST'>" in response.data
    # test going to courses/1 works, displays anything that might be unique to that course on the webpage

def test_course_update(client, auth):
    auth.login()

    # let's actually update that shit, submit a post request w/ data that will work
    response = client.post('/courses/1', data={
        'course': 'h',
        'course_number': 'h',
        'info': 'h',
    })
    # test that it redirects to courses
    assert response.headers['Location'] == 'http://localhost/courses'
    # let's check if response changed from that data being submitted
    response_2 = client.get('/courses')
    assert b'<li><a href="/courses/1">h</a></li>' in response_2.data
    other = client.post('/courses/1', data={
        'course': 'h',
        'course_number': '',
        'info': 'h',
    })
    print(other.data)
    assert b'<p>Course Number and Course fields required</p>' in other.data

def test_errors(client, auth):
    auth.login()
    response = client.get("/courses/270")

    assert b'<h1>Oh no!</h1>' in response.data
    assert b'<p>Page not found</p>' in response.data
    assert 404 == response.status_code

    with client:
        auth.login('student@stevenscollege.edu', 'asdfgh')
        response = client.get('/courses/1')
        # test that student got redirected home
        assert b'You are not permitted to view this page' in response.data