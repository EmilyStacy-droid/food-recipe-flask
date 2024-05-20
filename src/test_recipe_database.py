import unittest
from recipe_database import app, db
from recipe_database import RecipeDatabase, save_receipt_info

class TestRecipeDatabase(unittest.TestCase):

    def setUp(self):
        self.app = app
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.sqlite3'
        self.app.config['TESTING'] = True
        self.app_context = self.app.app_context()
        self.app_context.push()

        # Set up the database
        db.create_all()

    def tearDown(self):
        # Tear down the database and Flask application context
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_save_receipt_info(self):
        # Define test data
        recipe_list = [
            {'id': 1, 'title': 'Recipe 1', 'servings': 4, 'ready_in_min': 30, 'health_score': 8.5, 'cheap': False},
            {'id': 2, 'title': 'Recipe 2', 'servings': 2, 'ready_in_min': 45, 'health_score': 7.2, 'cheap': True}
        ]

        # Save recipe info to the database
        save_receipt_info(recipe_list)

        # Query the database to verify that the data was saved correctly
        saved_recipe = RecipeDatabase.RecipeInfo.query.filter_by(recipe_id=1).first()
        self.assertIsNotNone(saved_recipe)
        self.assertEqual(saved_recipe.title, 'Recipe 1')
        self.assertEqual(saved_recipe.servings, 4)

if __name__ == '__main__':
    unittest.main()
