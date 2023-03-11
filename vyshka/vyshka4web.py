from flask import Flask, render_template, request

from vyshka import Tournament

app = Flask(__name__)


@app.route('/search4', methods=['POST'])
def do_search() -> 'html':
    num_groups = request.form['num_groups']
    num_teams = request.form['num_teams']
    title = 'Here are your results:'
    tournament = Tournament(num_groups=num_groups, num_teams=num_teams)
    tournament.get_calendar()
    bracket_tour = tournament.generate_bracket()
    return render_template('results.html',
                           num_groups=num_groups,
                           num_teams=num_teams,
                           the_title=title,
                           the_results=bracket_tour, )


@app.route('/')
@app.route('/entry')
def entry_page() -> 'html':
    return render_template('entry.html', the_title='Welcome to vyshka on the web!')


if __name__ == '__main__':
    app.run(debug=True)