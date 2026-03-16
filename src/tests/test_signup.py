"""
Unit and integration tests for signup functionality.
Tests for POST /activities/{activity_name}/signup endpoint.
"""
import pytest


class TestSignupEndpoint:
    """Test suite for POST /activities/{activity_name}/signup endpoint."""

    def test_signup_successful(self, client):
        """POST /activities/{activity_name}/signup should successfully add participant."""
        activity_name = "Chess Club"
        email = "test_student@mergington.edu"
        
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert email in data["message"]
        assert activity_name in data["message"]

    def test_signup_non_existent_activity(self, client):
        """POST /activities/{non-existent}/signup should return 404."""
        response = client.post(
            "/activities/Non-Existent Club/signup",
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == 404
        data = response.json()
        assert "Activity not found" in data["detail"]

    def test_signup_duplicate_email(self, client):
        """POST /activities/{activity_name}/signup with duplicate email should return 400."""
        activity_name = "Chess Club"
        email = "michael@mergington.edu"  # Already signed up
        
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert response.status_code == 400
        data = response.json()
        assert "already signed up" in data["detail"].lower()

    def test_signup_new_student_added_to_participants(self, client):
        """Verify that a newly signed-up student appears in GET /activities."""
        activity_name = "Science Club"
        email = "new_student@mergington.edu"
        
        # Sign up the student
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200
        
        # Verify student is now in participants
        get_response = client.get("/activities")
        data = get_response.json()
        assert email in data[activity_name]["participants"]

    def test_signup_multiple_different_students(self, client):
        """Test signing up multiple different students to same activity."""
        activity_name = "Debate Team"
        email1 = "student1@mergington.edu"
        email2 = "student2@mergington.edu"
        
        # Sign up first student
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email1}
        )
        assert response1.status_code == 200
        
        # Sign up second student
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email2}
        )
        assert response2.status_code == 200
        
        # Verify both are in participants
        get_response = client.get("/activities")
        data = get_response.json()
        assert email1 in data[activity_name]["participants"]
        assert email2 in data[activity_name]["participants"]

    def test_signup_case_sensitive_activity_name(self, client):
        """Activity names should be case-sensitive."""
        response = client.post(
            "/activities/chess club/signup",  # Lowercase
            params={"email": "test@mergington.edu"}
        )
        assert response.status_code == 404


class TestSignupE2EWorkflow:
    """End-to-end workflow tests combining GET and POST."""

    def test_e2e_get_activities_then_signup(self, client):
        """E2E: Get activities list, then sign up for an activity."""
        # Step 1: Get all activities
        get_response = client.get("/activities")
        assert get_response.status_code == 200
        activities = get_response.json()
        assert len(activities) > 0
        
        # Step 2: Pick an activity and sign up
        activity_name = list(activities.keys())[0]
        email = "e2e_test@mergington.edu"
        
        signup_response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        assert signup_response.status_code == 200
        
        # Step 3: Verify signup in activities list
        get_response_after = client.get("/activities")
        assert get_response_after.status_code == 200
        updated_activities = get_response_after.json()
        assert email in updated_activities[activity_name]["participants"]

    def test_e2e_multiple_signups_workflow(self, client):
        """E2E: Sign up multiple students and verify all are registered."""
        activity_name = "Art Studio"
        emails = [
            "artist1@mergington.edu",
            "artist2@mergington.edu",
            "artist3@mergington.edu",
        ]
        
        # Sign up all students
        for email in emails:
            response = client.post(
                f"/activities/{activity_name}/signup",
                params={"email": email}
            )
            assert response.status_code == 200
        
        # Verify all are in the activity
        get_response = client.get("/activities")
        data = get_response.json()
        for email in emails:
            assert email in data[activity_name]["participants"]
