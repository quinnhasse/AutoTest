import git
from github import Github, GithubException
import os

class GitHubManager:
    def __init__(self, github_token):
        self.github_token = github_token
        self.github = Github(self.github_token)
        self.repo = None
        self.local_repo_path = 'ai_generated_repo'

    def clone_repository(self, repo_name):
        try:
            if os.path.exists(self.local_repo_path):
                # Remove the existing directory before cloning
                import shutil
                shutil.rmtree(self.local_repo_path)
            os.makedirs(self.local_repo_path, exist_ok=True)
            repo = self.github.get_repo(repo_name)
            git.Repo.clone_from(repo.clone_url, self.local_repo_path)
            self.repo = git.Repo(self.local_repo_path)
        except GithubException as e:
            print(f"Error accessing repository '{repo_name}': {e}")
            raise e
        except Exception as e:
            print(f"An error occurred while cloning the repository: {e}")
            raise e

    def add_submodule(self, submodule_url):
        self.repo.create_submodule(name='submodule', path='submodule', url=submodule_url)
        self.repo.git.add('.')  # Add changes
        self.repo.index.commit('Added submodule')
        self.repo.remote(name='origin').push()
        return 'The git submodule has been successfully added to your project.'

    def commit_and_push_changes(self, code_files, commit_message):
        repo_dir = os.path.abspath(self.local_repo_path)
        for filename, content in code_files:
            file_path = os.path.join(repo_dir, filename)
            # Ensure the directory exists
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, 'w') as f:
                f.write(content)
            # Add the file to the index using a path relative to the repo root
            relative_file_path = os.path.relpath(file_path, repo_dir)
            self.repo.index.add([relative_file_path])
        # Commit and push changes
        self.repo.index.commit(commit_message)
        origin = self.repo.remote(name='origin')
        origin.push()