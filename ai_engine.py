# pixcodeos/src/ryoiki_tenkai/ai_engine.py
import numpy as np
from sklearn.cluster import KMeans

class AIEngine:
    def __init__(self, n_clusters=2):
        """
        Initialize the AIEngine with an empty user data dictionary and a KMeans model.

        Parameters:
        n_clusters (int): The number of clusters for KMeans.
        """
        self.user_data = {}
        self.kmeans = KMeans(n_clusters=n_clusters)

    def track_user_behavior(self, user_id, behavior_data):
        """
        Track user behavior by adding behavior data to the user's data array.

        Parameters:
        user_id (str): The ID of the user.
        behavior_data (dict): A dictionary containing behavior data with keys "x" and "y".
        """
        try:
            if user_id not in self.user_data:
                self.user_data[user_id] = np.array([]).reshape(0, 2)  # Initialize as 2D array
            new_data = np.array([behavior_data["x"], behavior_data["y"]]).reshape(1, -1)  # Reshape to 2D array
            self.user_data[user_id] = np.vstack((self.user_data[user_id], new_data))
        except Exception as e:
            print(f"Error tracking user behavior: {e}")

    def analyze_behavior(self, user_id):
        """
        Analyze user behavior using KMeans clustering.

        Parameters:
        user_id (str): The ID of the user.

        Returns:
        dict: A dictionary containing the clusters if analysis is successful, otherwise an empty dictionary.
        """
        try:
            if user_id in self.user_data and len(self.user_data[user_id]) > 1:
                clusters = self.kmeans.fit_predict(self.user_data[user_id])
                return {"clusters": clusters}
            return {}
        except Exception as e:
            print(f"Error analyzing behavior: {e}")
            return {}

    def get_user_data(self, user_id):
        """
        Get the behavior data for a specific user.

        Parameters:
        user_id (str): The ID of the user.

        Returns:
        np.ndarray: The behavior data of the user.
        """
        return self.user_data.get(user_id, np.array([]))

    def reset_user_data(self, user_id):
        """
        Reset the behavior data for a specific user.

        Parameters:
        user_id (str): The ID of the user.
        """
        self.user_data[user_id] = np.array([]).reshape(0, 2)

if __name__ == "__main__":
    ai_engine = AIEngine()
    ai_engine.track_user_behavior("user1", {"x": 1, "y": 2})
    ai_engine.track_user_behavior("user1", {"x": 3, "y": 4})
    print("User Data:", ai_engine.get_user_data("user1"))
    print("Behavior Analysis:", ai_engine.analyze_behavior("user1"))
    ai_engine.reset_user_data("user1")
    print("User Data after reset:", ai_engine.get_user_data("user1"))
