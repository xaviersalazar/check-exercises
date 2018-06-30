import git, pathlib, os, re, shutil, time, sys

# Requires:
# --Python3
# --GitPython


class Progress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=None):
        for i, line in enumerate(self._cur_line):
            time.sleep(0.0015)
            printProgressBar(i + 1, len(self._cur_line), prefix='Cloning:', length=50)
            sys.stdout.write('\r')
            sys.stdout.flush()


def printProgressBar (iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')


def createPath():
    pathName = str(pathlib.Path.home()) + '/Desktop/tmp/'
    pathlib.Path(pathName).mkdir(parents=True, exist_ok=True)
    return pathName


def clone(p):
    codeup = r"codeup-web-exercises"
    while True:
        remoteURL = input('Enter your remote github repo: ')
        matches = re.findall(codeup, remoteURL)
        if not matches:
            print('Not the correct repo. Use your codeup-web-exercises repo')
            print('SSH ex: git@github.com:your-name-here/codeup-web-exercises.git')
            print('HTTPS ex: https://github.com/your-name-here/codeup-web-exercises.git\n')
        else:
            print('---------- Cloning Repo ----------')
            git.Repo.clone_from(remoteURL, p, progress=Progress())
            break
    print('\n----------- DONE CLONING ----------\n\n')


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