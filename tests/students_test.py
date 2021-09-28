def test_get_assignments_student_1(client, h_student_1):
    response = client.get(
        '/student/assignments',
        headers=h_student_1
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 1


def test_get_assignments_student_2(client, h_student_2):
    response = client.get(
        '/student/assignments',
        headers=h_student_2
    )

    assert response.status_code == 200

    data = response.json['data']
    for assignment in data:
        assert assignment['student_id'] == 2

def test_get_assignments_invalid_student(client, h_invalid_student):
    response = client.get(
        '/student/assignments',
        headers=h_invalid_student
    )

    assert response.status_code == 400

def test_get_assignments_teacher_2(client, h_teacher_2):
    """
    failure case: if teacher tries to submit assignment throw 403
    """
    response = client.get(
        '/student/assignments',
        headers=h_teacher_2
    )

    assert response.status_code == 403
    data = response.json

    assert data['error'] == "FyleError"


def test_post_assignment_student_1(client, h_student_1):
    content = 'ABCD TESTPOST'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None

def test_update_assignment_student_1(client, h_student_1):
    content = 'ABCD UPDATE'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id' : 2,
            'content': content
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['content'] == content
    assert data['state'] == 'DRAFT'
    assert data['teacher_id'] is None


def test_update_submitted_assignment_student_1(client, h_student_1):
    """
    failure case: try to update submitted assignment
    """
    content = 'ABCD UPDATE'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id' : 1,
            'content': content
        })

    assert response.status_code == 400
    data = response.json

    assert data['error'] == "FyleError"

def test_update_others_assignment_student_1(client, h_student_1):
    """
    failure case: try to update other students assignment
    """
    content = 'ABCD UPDATE'

    response = client.post(
        '/student/assignments',
        headers=h_student_1,
        json={
            'id' : 3,
            'content': content
        })

    assert response.status_code == 400
    data = response.json

    assert data['error'] == "FyleError"


def test_submit_assignment_student_1(client, h_student_1):
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 2,
            'teacher_id': 2
        })

    assert response.status_code == 200

    data = response.json['data']
    assert data['student_id'] == 1
    assert data['state'] == 'SUBMITTED'
    assert data['teacher_id'] == 2

def test_submit_others_assignment_student_1(client, h_student_1):
    """
    failure case: student tries to submit others assignment
    """
    response = client.post(
        '/student/assignments/submit',
        headers=h_student_1,
        json={
            'id': 3,
            'teacher_id': 2
        })

    assert response.status_code == 400
    data = response.json

    assert data['error'] == "FyleError"
