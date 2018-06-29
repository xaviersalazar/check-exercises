import git, pathlib, os, re, shutil

# Requires:
# --Python3
# --GitPython

class Progress(git.remote.RemoteProgress):
    def update(self, *args):
        print('----------- CLONING REPO ----------')
        print(self._cur_line)

def createPath():
    pathName = str(pathlib.Path.home()) + '/Desktop/tmp/'
    pathlib.Path(pathName).mkdir(parents=True, exist_ok=True)
    return pathName

def clone(p):
    remoteURL = input('Enter your remote github repo: ')
    git.Repo.clone_from(remoteURL, p, progress=Progress())
    print('----------- DONE CLONING ----------\n\n')

def filter(p):
    regex = r'\.html|\.js|\.css'
    gitExercises = []
    for subdir, dirs, files in os.walk(p):
        for file in files:
            matches = re.findall(regex, file)
            if matches:
                gitExercises.append(file)
    shutil.rmtree(p)
    return gitExercises

def checkMissing(exer, gExer):
    missing = list(set(exer)-set(gExer))
    if not missing:
        print('Your not missing any files')
    else:
        print('Your missing: ')
        print('\n'.join(missing))


exercises = ['welcome.html', 'github.html', 'forms.html', 'style.css', 'css_selectors.html', 'selectors.css', 'login-form.html', 'login.css', 'messages.html', 'messages.css', 'twitter.html', 'twitter.css', 'media-queries.html', 'media-queries.css', 'grid-layout.html', 'grid-layout.css', 'order-pizza.html', 'custom.css', 'inline_js.html', 'external_js.html', 'external.js', 'functions.js', 'functions_js.html', 'conditionals.js', 'conditionals.html', 'loops.html', 'while.js', 'for_loops.js', 'break_and_continue.js', 'iterating.js', 'iterating_arrays_js.html', 'planets-array.js', 'planets-js.html', 'planets-string.js', 'split-join.html', 'objects.js', 'objects.html', 'circle.js', 'math-js.html', 'defuse-the-bom.html', 'dom-query-js.html']

path = createPath()
clone(path)
gitExer = filter(path)
checkMissing(exercises, gitExer)