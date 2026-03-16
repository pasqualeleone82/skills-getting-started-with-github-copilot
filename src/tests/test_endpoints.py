"""
Unit and integration tests for FastAPI app endpoints.
Tests for GET /activities and response structure validation.
"""
import pytest


class TestGetActivitiesEndpoint:
    """Test suite for GET /activities endpoint."""

    def test_get_activities_returns_200(self, client):
        """GET /activities should return 200 OK."""
        response = client.get("/activities")
        assert response.status_code == 200

    def test_get_activities_returns_dict(self, client):
        """GET /activities should return a dictionary of activities."""
        response = client.get("/activities")
        data = response.json()
        assert isinstance(data, dict)

    def test_get_activities_returns_non_empty(self, client):
        """GET /activities should return non-empty list of activities."""
        response = client.get("/activities")
        data = response.json()
        assert len(data) > 0

    def test_get_activities_contains_expected_activities(self, client):
        """GET /activities should contain specific known activities."""
        response = client.get("/activities")
        data = response.json()
        expected_activities = [
            "Chess Club",
            "Programming Class",
            "Gym Class",
            "Basketball Team",
            "Tennis Club",
            "Drama Club",
            "Art Studio",
            "Debate Team",
            "Science Club",
        ]
        for activity in expected_activities:
            assert activity in data

    def test_activity_has_required_fields(self, client):
        """Each activity should have required fields: description, schedule, max_participants, participants."""
        response = client.get("/activities")
        data = response.json()
        required_fields = {"description", "schedule", "max_participants", "participants"}
        
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data, dict)
            assert required_fields.issubset(set(activity_data.keys())), \
                f"Activity '{activity_name}' missing required fields"

    def test_activity_participants_is_list(self, client):
        """Each activity's participants field should be a list."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["participants"], list), \
                f"Activity '{activity_name}' participants is not a list"

    def test_activity_max_participants_is_int(self, client):
        """Each activity's max_participants should be an integer."""
        response = client.get("/activities")
        data = response.json()
        
        for activity_name, activity_data in data.items():
            assert isinstance(activity_data["max_participants"], int), \
                f"Activity '{activity_name}' max_participants is not an int"

    def test_root_redirect_to_static(self, client):
        """GET / should redirect to /static/index.html."""
        response = client.get("/", follow_redirects=False)
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"
