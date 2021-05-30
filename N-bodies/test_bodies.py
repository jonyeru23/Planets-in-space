import pytest
from bodies import *


@pytest.fixture(scope='module')
def objects():
    objects = {
        'board': Board(),
        'body': Planet((4 / (3 * pi)), 1, 1, 1),
        'body1': Planet(2, 1, 1, np.array([1, 1])),
        'body2': Planet(2, 2, 1, np.array([3, 4])),
        'body3': Planet(3, 4, 6, np.array([7, 9])),
        'body4': Planet(3, 7, 1, np.array([7, 9]))
    }
    objects['board'].set_up()
    yield objects


def test_running(objects):
    assert objects['board'].is_running() is True

    objects['board'].terminate()
    assert objects['board'].is_running() is False


def test_radius(objects):
    assert objects['body']._get_radius() == 1


def test_Fg(objects):
    assert objects['body1'].force_scalar_by(objects['body2']) == 4 * G


def test_distance(objects):
    assert objects['body1'].distance_from(objects['body2']) == 1


def test_force_direction_vector(objects):
    assert np.array_equal(np.array([-1, 0]), objects['body1'].get_unit_vector_to(objects['body2']))

    unit_vector = objects['body3'].get_unit_vector_to(objects['body4'])
    assert round(np.sqrt(unit_vector.dot(unit_vector))) == 1


def test_acceleration(objects):
    F = objects['body3'].get_force(objects['body4'])
    A = objects['body3'].get_acceleration(F)
    assert np.array_equal(A, np.true_divide(F, objects['body3'].mass))

    F = objects['body1'].get_force(objects['body4'])
    A = objects['body1'].get_acceleration(F)
    assert np.array_equal(A, np.true_divide(F, objects['body1'].mass))


def test_adding_arrays():
    zeros = np.zeros(2)
    ones = np.ones(2)
    assert np.array_equal(zeros + ones, ones)


def test_change_speed(objects):
    combined_forces = np.zeros(2)
    body1 = objects['body1']
    list_of_bodies = [
        objects['body2'],
        objects['body3'],
        objects['body4']
    ]
    for body_i in list_of_bodies:
        combined_forces = np.add(combined_forces, body1.get_force(body_i))
    initial_speed = body1.V
    body1.change_speed(combined_forces)
    assert not np.array_equal(initial_speed,  body1.V)
    assert not np.isnan(combined_forces).any()


def test_change_position():
    body5 = Planet(4, 0, 0, np.array([1, 0], dtype=float))
    body5.change_position()
    assert np.array_equal(body5.position, np.array([1, 0], dtype=float))

def test_get_random_nums():
    color = np.random.randint(255, size=3)
    print(tuple(color))



