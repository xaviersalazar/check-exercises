import git, pathlib, os, re, shutil, time, sys

# Requires:
# --Python3
# --GitPython

# Github cloning progress
class Progress(git.remote.RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=None):
        for i, line in enumerate(self._cur_line):
            time.sleep(0.0015)
            printProgressBar(i + 1, len(self._cur_line), prefix='Cloning:', length=50)
            sys.stdout.write('\r')
            sys.stdout.flush()

# Progress bar for cloning
def printProgressBar (iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█'):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print('\r%s |%s| %s%% %s' % (prefix, bar, percent, suffix), end='\r')

# Create temp folder
def createPath():
    pathName = str(pathlib.Path.home()) + '/Desktop/tmp/'
    pathlib.Path(pathName).mkdir(parents=True, exist_ok=True)
    return pathName

# Clone github repo
# Check for validation
def clone(p):
    codeup = r'codeup-web-exercises'
    while True:
        remoteURL = input('Enter your remote github repo: ')
        matches = re.findall(codeup, remoteURL)
        if not matches:
            print('Not the correct repo. Use your codeup-web-exercises repo')
            print('SSH ex: git@github.com:your-name-here/codeup-web-exercises.git')
            print('HTTPS ex: https://github.com/your-name-here/codeup-web-exercises.git\n')
        else:
            git.Repo.clone_from(remoteURL, p, progress=Progress())
            break
    print('\n----------- DONE CLONING ----------\n\n')

# Filter out any unnecessary files from github clone
# Remove tmp folder after list is created
def filter(p):
    regex = r'\.html|\.js|\.css|\.java|\.sql'
    gitExercises = []
    for subdir, dirs, files in os.walk(p):
        for file in files:
            matches = re.findall(regex, file)
            if matches:
                gitExercises.append(file)
    shutil.rmtree(p)
    return gitExercises

# Check missing files list against master dictionary for any differences
# Separate files by extension
def checkMissing(exer, gExer):
    bigList = []
    htmlReg, cssReg, jsReg, javaReg, sqlReg = r'\.html', r'\.css', r'\.js', r'\.java', r'\.sql'
    html, css, js, java, sql = [], [], [], [], []

    for key, value in exer.items():
        for item in value:
            bigList.append(item)
    missing = list(set(bigList)-set(gExer))

    for file in missing:
        if re.findall(htmlReg, file):
            html.append(file)
        elif re.findall(cssReg, file):
            css.append(file)
        elif re.findall(jsReg, file):
            js.append(file)
        elif re.findall(javaReg, file):
            java.append(file)
        elif re.findall(sqlReg, file):
            sql.append(file)

    if not missing:
        print('Your not missing any files')
    else:
        printMissing(html, css, js, java, sql)

# Print formatted missing list
def printMissing(h, c, j, jv, s):
    print('Your missing:\n')
    print('HTML:')
    print('---{}\n'.format('\n---'.join(h)))
    print('CSS:')
    print('---{}\n'.format('\n---'.join(c)))
    print('JAVASCRIPT:')
    print('---{}\n'.format('\n---'.join(j)))
    print('JAVA:')
    print('---{}\n'.format('\n---'.join(jv)))
    print('MYSQL:')
    print('---{}\n'.format('\n---'.join(s)))

# Master dictionary
exercises = {
    'HTML': ['welcome.html',
             'forms.html',
             'css_selectors.html',
             'css_box_model.html',
             'css_positioning.html',
             'media-queries.html',
             'grid-layout.html',
             'order-pizza.html',
             'inline_js.html',
             'external_js.html',
             'functions_js.html',
             'conditionals.html',
             'loops.html',
             'iterating_arrays_js.html',
             'planets-js.html',
             'split-join.html',
             'objects.html',
             'math-js.html',
             'defuse-the-bom.html',
             'dom-query-js.html',
             'google_maps_api.html',
             'jquery_exercises.html',
             'konami.html',
             'jquery_faq.html',
             'ajax-store.html',
             'ajax-blog.html',
             'weather_map.html'],
    'CSS': ['style.css',
            'selectors.css',
            'box_model.css',
            'positioning.css',
            'media-queries.css',
            'grid-layout.css'],
    'JAVASCRIPT': ['external.js',
                   'functions.js',
                   'conditionals.js',
                   'while.js',
                   'for_loops.js',
                   'break_and_continue.js',
                   'iterating.js',
                   'planets-array.js',
                   'planets-string.js',
                   'objects.js',
                   'circle.js',
                   'es6.js',
                   'map-filter-reduce.js',
                   'promises.js'],
    'JSON': ['inventory.json',
             'blog.json'],
    'JAVA': ['HelloWorld.java',
             'ConsoleExercises.java',
             'ControlFlowExercises.java',
             'StringExercise.java',
             'MethodsExercises.java',
             'HighLow.java',
             'Person.java',
             'Input.java',
             'Circle.java',
             'CircleApp.java',
             'ServerNameGenerator.java',
             'Movie.java',
             'MoviesArray.java',
             'MoviesApplication.java',
             'Rectangle.java',
             'Square.java',
             'ShapesTest.java',
             'Shape.java',
             'Measurable.java',
             'Quadrilateral.java',
             'Student.java',
             'GradesApplication.java'],
    'MYSQL': ['albums_migration.sql',
              'albums_seeder.sql',
              'aliases_exercises.sql',
              'delete_exercises.sql',
              'functions_exercises.sql',
              'group_by_exercises.sql',
              'join_exercises.sql',
              'limit_exercises.sql',
              'order_by_exercises.sql',
              'select_exercises.sql',
              'subqueries_exercises.sql',
              'update_exercises.sql',
              'where_exercises.sql']
}

path = createPath()
clone(path)
gitExer = filter(path)
checkMissing(exercises, gitExer)