We have a Jenkins service that will perform CICD for this package.
We use a Jenkins Shared Library, as seen in the Jenkinsfile.

## Deployment Workflow

Continuous integration (CI) and continuous delivery (CD) is based on Pull Requests.
The workflow is very simple:

1. `git push` a new branch to the Source Control Management (SCM) server.
2. Log in to the SCM server and create a pull request.
    * CI runs at this point (running all automated tests).
3. Once CI has completed, **merge** the Pull Request
    * CD runs at this point (deploying to the appropriate Python Package Index)

> Once CD completes, it is wise to ensure you can download the package from the Python Package Index where the package lives.