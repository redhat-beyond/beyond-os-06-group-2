from django.db.models.query import QuerySet
import pytest
from tasks.models import Priority, Task, Status
from users.models import User, Team, Role

pytestmark = pytest.mark.django_db


class DBPrepare:
    """
    Create an employee test user
    """
    @staticmethod
    def create_example_employee(username):
        team = Team.objects.first()
        employee = User.create_user(username=username,
                                    email="example@gmail.com",
                                    password='xsdDS23',
                                    first_name="Test",
                                    last_name="Test",
                                    role=Role.EMPLOYEE,
                                    team=team)
        return employee

    """
    Create a manager test user
    """
    @staticmethod
    def create_example_manager(username):
        team = Team.objects.first()
        manager = User.create_user(username=username,
                                   email="example@gmail.com",
                                   password='xsdDS23',
                                   first_name="Test",
                                   last_name="Test",
                                   role=Role.MANAGER,
                                   team=team)
        return manager

    """
    Create a test team
    """
    @staticmethod
    def create_example_team():
        team = Team.objects.create(name="TestTeam", description="Test Team")
        return team

    """
    Create a test task
    """
    @staticmethod
    def create_example_task(assignee, assigner, priority, status):
        title = "Test task"
        description = 'Test'
        task = Task.objects.create(
                                    title=title,
                                    created_by=assigner,
                                    assignee=assignee,
                                    status=status,
                                    priority=priority,
                                    description=description)
        return task


@pytest.mark.django_db
class TestTasksFilters:
    """
    Add test data to database
    """
    @pytest.fixture
    def prepare_database(self):
        DBPrepare.create_example_team()
        manager = DBPrepare.create_example_manager("TestManager")
        for i in range(5):
            employee = DBPrepare.create_example_employee(f'TestUser{i}')
            DBPrepare.create_example_task(employee, manager, Priority.LOW, Status.BACKLOG)
            DBPrepare.create_example_task(employee, manager, Priority.MEDIUM, Status.IN_PROGRESS)
            DBPrepare.create_example_task(employee, manager, Priority.HIGH, Status.DONE)

    """
    Test filtering tasks by priority
    """
    def test_priority_filter(self, prepare_database):
        for priority in (Priority.LOW, Priority.HIGH, Priority.MEDIUM):
            filtered_tasks = Task.filter_by_symbol(priority)
            assert isinstance(filtered_tasks, QuerySet)
            assert all(isinstance(task, Task) for task in filtered_tasks)
            assert len(filtered_tasks) == 5
            assert all(p == priority for p in filtered_tasks.values_list('priority', flat=True))

    """
    Test that it is impossible to filter using invalid value
    """
    def test_invalid_priority_filter(self, prepare_database):
        with pytest.raises(ValueError):
            Task.filter_by_symbol('INVALID')

    """
    Test filtering tasks by asignee id
    """
    def test_assignee_filter(self, prepare_database):
        filtered_tasks = Task.filter_by_assignee(2)
        assert isinstance(filtered_tasks, QuerySet)
        assert all(isinstance(task, Task) for task in filtered_tasks)
        assert len(filtered_tasks) == 3
        assert all(assignee_id == 2 for assignee_id in filtered_tasks.values_list('assignee', flat=True))

    """
    Test that it is impossible to filter using invalid value
    """
    def test_invalid_assignee_filter(self):
        with pytest.raises(ValueError):
            Task.filter_by_assignee(-2)
        with pytest.raises(TypeError):
            Task.filter_by_assignee('INVALID')

    """
    Test filtering tasks by status
    """
    def test_status_filter(self, prepare_database):
        for status in Status:
            filtered_tasks = Task.filter_by_status(status)
            assert isinstance(filtered_tasks, QuerySet)
            assert all(isinstance(task, Task) for task in filtered_tasks)
            assert len(filtered_tasks) == 5
            assert all(s == status for s in filtered_tasks.values_list('status', flat=True))

    """
    Test that it is impossible to filter using invalid value
    """
    def test_invalid_status_filter(self, prepare_database):
        with pytest.raises(ValueError):
            Task.filter_by_status('INVALID')
