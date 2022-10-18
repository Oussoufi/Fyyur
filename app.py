#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#


from operator import itemgetter
import dateutil.parser
import babel
from datetime import datetime
from flask import Flask, render_template, request,jsonify, flash, redirect, url_for, abort
import re
import logging
from logging import Formatter, FileHandler, error
from forms import *
from datetime import datetime
from models import Venue, Artist, Show, db, moment, migrate


#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#



def create_app(config_file):
    app = Flask(__name__)
    app.config.from_object(config_file)
    moment.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    


    #----------------------------------------------------------------------------#
    # Filters.
    #----------------------------------------------------------------------------#

    def format_datetime(value, format='medium'):
      date = dateutil.parser.parse(value)
      if format == 'full':
          format="EEEE MMMM, d, y 'at' h:mma"
      elif format == 'medium':
          format="EE MM, dd, y h:mma"
      return babel.dates.format_datetime(date, format, locale='en')

    app.jinja_env.filters['datetime'] = format_datetime

    #----------------------------------------------------------------------------#
    # Controllers.
    #----------------------------------------------------------------------------#

    @app.route('/')
    def index():
      return render_template('pages/home.html')


    #  Venues
    #  ----------------------------------------------------------------

    @app.route('/venues')
    def venues():
      # TODO: replace with real venues data.
      #       num_upcoming_shows should be aggregated based on number of upcoming shows per venue.


      venue_datas = Venue.query.join(Show, Show.venue_id == Venue.id).all()
      
      query_locations= db.session.query(Venue.city, Venue.state).order_by(Venue.state).all()

      
      data = []
      

      for location in query_locations:
        city=location[0]
        state=location[1]
        num_upcoming_shows = 0
        venues=[]
        if venue_datas is not None: 
          for venue in venue_datas:
    
            if ((venue.city == city) and (venue.state == state)):
              for show in venue.shows:
                print(show)
                if  show.start_time > datetime.now():
                  num_upcoming_shows += 1
                  venues.append({
                      "id": show.venue_id,
                      "name": show.venue.name,
                      "num_upcoming_shows": num_upcoming_shows
                  })
                  print("venues = ",venues)
                else:
                   num_upcoming_shows = 0
  
          data.append({
                "city": city,
                "state":state,
                "venues": venues,

                  })
          print("data ",data)

      
        
      return render_template('pages/venues.html', areas=data)
         
    # Search Venue
    #  ----------------------------------------------------------------

    @app.route('/venues/search', methods=['POST'])
    def search_venues():
      # TODO: implement search on venues with partial string search. Ensure it is case-insensitive.
      # seach for Hop should return "The Musical Hop".
      # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
      search_term = request.form.get('search_term', '')
      search_term_venues = Venue.query.filter(Venue.name.ilike('%' +search_term+ '%')).all()
      list_venues = []
      now = datetime.now()
      for venue in search_term_venues:
          venue_by_shows = Show.query.filter_by(venue_id=venue.id).all()
          num_upcoming = 0
          for show in venue_by_shows:
              if show.start_time > now:
                  num_upcoming += 1

          list_venues.append({
              "id": venue.id,
                "name": venue.name,
                "num_upcoming_shows": num_upcoming 
            })

      response = {
          "count": len(search_term_venues),
          "data": list_venues
        }
        # response={
        #     "count": 1,
        #     "data": [{
        #       "id": 2,
        #       "name": "The Dueling Pianos Bar",
        #       "num_upcoming_shows": 0,
        #     }] 
        #   }
      return render_template('pages/search_venues.html', results=response, search_term=request.form.get('search_term', ''))

    #  Show Venue
    #  ----------------------------------------------------------------

    @app.route('/venues/<int:venue_id>')
    def show_venue(venue_id):
      # shows the venue page with the given venue_id
      # TODO: replace with real venue data from the venues table, using venue_id

      venue = Venue.query.get_or_404(venue_id)
      print(venue)

      upcoming_shows_count=0
      upcoming_shows = []
      past_shows = []
      past_shows_count= 0
      data = {}
      now = datetime.now()
      # past shows per venue
      past_shows_query = db.session.query(Show)\
        .join(Venue)\
          .filter(Show.venue_id == venue.id)\
            .filter(Show.start_time< now).all()

      for show in past_shows_query:
          past_shows_count += 1
          past_shows.append({
            "artist_id": show.artist_id,
            "artist_name": show.artist.name,
            "artist_image_link": show.artist.image_link,
            "start_time": format_datetime(str(show.start_time))
          })
      # upcoming shows per venue
      upcoming_shows_query = db.session.query(Show)\
        .join(Venue)\
          .filter(Show.venue_id == venue.id)\
            .filter(Show.start_time>now).all()

      for show in upcoming_shows_query:
        upcoming_shows_count += 1
        upcoming_shows.append({
          "artist_id": show.artist_id,
          "artist_name": show.artist.name,
          "artist_image_link": show.artist.image_link,
          "start_time": format_datetime(str(show.start_time))
          })

      
      if data is not None:    
        data={
          "id": venue.id,
          "name": venue.name,
          "genres": venue.genres,
          "address": venue.address,
          "city": venue.city,
          "state": venue.state,
          "phone": venue.phone,
          "website": venue.website_link,
          "facebook_link": venue.facebook_link,
          "seeking_talent": venue.seeking_talent,
          "seeking_description": venue.seeking_description,
          "image_link": venue.image_link,
          "past_shows": past_shows,
          "upcoming_shows": upcoming_shows,
          "past_shows_count": past_shows_count,
          "upcoming_shows_count": upcoming_shows_count,
        }
      else:
        flash("No Data Available in Database")

      return render_template('pages/show_venue.html', venue=data)

    #  Create Venue
    #  ----------------------------------------------------------------

    @app.route('/venues/create', methods=['GET'])
    def create_venue_form():
      form = VenueForm()
      return render_template('forms/new_venue.html', form=form)

    @app.route('/venues/create', methods=['POST'])
    def create_venue_submission():
      form = VenueForm()
      if form.validate_on_submit():
        name = form.name.data
        city = form.city.data
        state = form.state.data
        address = form.address.data
        phone = form.phone.data 
        phone = re.sub('\D', '', phone) 
        genres = form.genres.data
        seeking_talent = form.seeking_talent.data
        seeking_description = form.seeking_description.data
        image_link = form.image_link.data
        website_link = form.website_link.data
        facebook_link = form.facebook_link.data
        
        venue = Venue(name=name, city=city, state=state, address=address, phone=phone, genres=genres, \
          seeking_talent=seeking_talent, seeking_description=seeking_description, image_link=image_link, \
            website_link=website_link, facebook_link=facebook_link)

        db.session.add(venue)
        db.session.commit()
        flash('Venue ' + request.form['name'] + ' was successfully listed!')
        return redirect(url_for('index'))

      if form.errors:
        flash(form.errors)
        return redirect(url_for('create_venue_submission'))
      return render_template('pages/home.html')

    #  Delete Venue
    #  ----------------------------------------------------------------

    @app.route('/venues/<venue_id>', methods=['DELETE'])
    def delete_venue(venue_id):
      # TODO: Complete this endpoint for taking a venue_id, and using
      # SQLAlchemy ORM to delete a record. Handle cases where the session commit could fail.
      error = False
      try:
        venue = Venue.query.get(venue_id)
        db.session.delete(venue)
        db.session.commit()
      except:
        db.session.rollback()
        error = True
      finally:
        db.session.close()
        if error:
          abort(500)
        else:
          return jsonify({'delete success': True})


      # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
      # clicking that button delete it from the db then redirect the user to the homepage
        

    #  Artists
    #  ----------------------------------------------------------------
    @app.route('/artists')
    def artists():
      # TODO: replace with real data returned from querying the database
      artists = Artist.query.order_by(Artist.name).all()
      data = []
      for artist in artists:
          data.append({
              "id": artist.id,
                "name": artist.name,
            })

        # data=[{
        #   "id": 4,
        #   "name": "Guns N Petals",
        # }, {
        #   "id": 5,
        #   "name": "Matt Quevedo",
        # }, {
        #   "id": 6,
        #   "name": "The Wild Sax Band",
        # }]
      return render_template('pages/artists.html', artists=data)

    #  Search Artist
    #  ----------------------------------------------------------------

    @app.route('/artists/search', methods=['POST'])
    def search_artists():
      # TODO: implement search on artists with partial string search. Ensure it is case-insensitive.
      # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
      # search for "band" should return "The Wild Sax Band".
      search_term = request.form.get('search_term', '')
      artists = Artist.query.filter(Artist.name.ilike('%' +search_term+ '%')).all()

      print(artists)
      list_artists = []
      now = datetime.now()
      for artist in artists:
          num_upcoming = 0
          for show in artist.shows:
              if show.start_time > now:
                  num_upcoming += 1

          list_artists.append({
              "id": artist.id,
                "name": artist.name,
                "num_upcoming_shows": num_upcoming
            })

      response = {
          "count": len(artists),
          "data": list_artists
        }

      # response={
      #   "count": 1,
      #   "data": [{
      #     "id": 4,
      #     "name": "Guns N Petals",
      #     "num_upcoming_shows": 0,
      #   }]
      # }
      return render_template('pages/search_artists.html', results=response, search_term=search_term)

    #  show Artist
    #  ----------------------------------------------------------------

    @app.route('/artists/<int:artist_id>')
    def show_artist(artist_id):
      # shows the artist page with the given artist_id
      # TODO: replace with real artist data from the artist table, using artist_id
      artist = Artist.query.get_or_404(artist_id)
      past_shows = []
      past_shows_count = 0
      upcoming_shows = []
      upcoming_shows_count = 0
      
      current_date = datetime.now()

      # past shows per venue
      upcoming_shows_query = db.session.query(Show)\
        .join(Artist)\
          .filter(Show.artist_id == artist.id)\
            .filter(Show.start_time > current_date).all()
      for show in upcoming_shows_query:
              upcoming_shows_count += 1
              upcoming_shows.append({
                  "venue_id": show.venue_id,
                  "venue_name": show.venue.name,
                  "venue_image_link": show.venue.image_link,
                  "start_time": format_datetime(str(show.start_time))
              })


      # past shows per venue
      past_shows_query = db.session.query(Show)\
        .join(Artist)\
          .filter(Show.artist_id == artist.id)\
            .filter(Show.start_time< current_date).all()
      for show in past_shows_query:
          past_shows_count += 1
          past_shows.append({
              "venue_id": show.venue_id,
              "venue_name": show.venue.name,
              "venue_image_link": show.venue.image_link,
              "start_time": format_datetime(str(show.start_time))
            })


      data = {
        "id": artist.id,
        "name": artist.name,
        "genres": [genre for genre in artist.genres],
        "city": artist.city,
        "state": artist.state,
        "phone": artist.phone,
        "website_link": artist.website_link,
        "facebook_link": artist.facebook_link,
        "seeking_venue": artist.seeking_venue,
        "seeking_description": artist.seeking_description,
        "image_link": artist.image_link,
        "past_shows": past_shows,
        "past_shows_count": past_shows_count,
        "upcoming_shows_count": upcoming_shows_count,
        "upcoming_shows": upcoming_shows,
      }
      return render_template('pages/show_artist.html', artist=data)

    #  Update
    #  ----------------------------------------------------------------



    # Edit Artist Submission Method
    #------------------------------------------------------------------

    @app.route('/artists/<int:artist_id>/edit', methods=['GET','POST'])
    def edit_artist_submission(artist_id):
      # TODO: take values from the form submitted, and update existing
      # artist record with ID <artist_id> using the new attributes
      artist = Artist.query.get_or_404(artist_id)
      if artist is None:
        abort(404)
      
      form = ArtistForm(obj=artist)
      if form.validate_on_submit():
        form.populate_obj(obj=artist)
        db.session.commit()
        flash('Artist is successfully updated')
        return redirect(url_for('show_artist', artist_id=artist.id))
      return render_template('forms/edit_artist.html', form=form, artist=artist)

    # Edit Venue Submission Method
    #---------------------------------------------------------------------

    @app.route('/venues/<int:venue_id>/edit', methods=['GET','POST'])
    def edit_venue_submission(venue_id):
      # TODO: take values from the form submitted, and update existing
      # venue record with ID <venue_id> using the new attributes
      # TODO: take values from the form submitted, and update existing
      # artist record with ID <artist_id> using the new attributes
      venue = Venue.query.get_or_404(venue_id)
      if venue is None:
        abort(404)
      
      form = VenueForm(obj=venue)
      if form.validate_on_submit():
        form.populate_obj(obj=venue)
        db.session.commit()
        flash('Venue is successfully updated')
        return redirect(url_for('show_venue', venue_id=venue.id))
      return render_template('forms/edit_venue.html', form=form, venue=venue)

    #  Create Artist
    #  ----------------------------------------------------------------

    @app.route('/artists/create', methods=['GET'])
    def create_artist_form():
      form = ArtistForm()
      return render_template('forms/new_artist.html', form=form)

    @app.route('/artists/create', methods=['GET','POST'])
    def create_artist_submission():
      # called upon submitting the new artist listing form
      # TODO: insert form data as a new Venue record in the db, instead
      # TODO: modify data to be the data object returned from db insertion
      form = ArtistForm()

      if form.validate_on_submit():
        # on successful db insert, flash success
        name = form.name.data
        city = form.city.data
        state = form.state.data
        phone = form.phone.data
        genres =form.genres.data
        genres= list(genres)
        image_link = form.image_link.data
        website_link = form.website_link.data
        facebook_link = form.facebook_link.data
        seeking_venue =  form.seeking_venue.data
        seeking_description = form.seeking_description.data

        artist = Artist(name=name, city=city, state=state, phone=phone,\
          genres=genres, image_link=image_link, website_link=website_link, \
            facebook_link=facebook_link, seeking_venue=seeking_venue, seeking_description=seeking_description)
        db.session.add(artist)
        db.session.commit()
        print(artist)
        flash('Artist ' + request.form['name'] + ' was successfully listed!')
        return redirect(url_for('index'))
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Artist ' + data.name + ' could not be listed.')
      if form.errors:
        flash(form.errors)
        return redirect(url_for('create_artist_submission'))
      return render_template('pages/home.html')


    #  Shows
    #  ----------------------------------------------------------------

    @app.route('/shows')
    def shows():
      # displays list of shows at /shows
      # TODO: replace with real venues data.
      shows = Show.query.all()

      data = []
      for show in shows:
        fetch_show = {
          "venue_id": show.venue_id,
          "venue_name": show.venue.name,
          "artist_id": show.artist_id,
          "artist_name": show.artist.name,
          "artist_image_link": show.artist.image_link,
          "start_time":format_datetime(str(show.start_time))
        }
        data.append(fetch_show)
      

      # data=[{
      #   "venue_id": 1,
      #   "venue_name": "The Musical Hop",
      #   "artist_id": 4,
      #   "artist_name": "Guns N Petals",
      #   "artist_image_link": "https://images.unsplash.com/photo-1549213783-8284d0336c4f?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=300&q=80",
      #   "start_time": "2019-05-21T21:30:00.000Z"
      # }, {
      #   "venue_id": 3,
      #   "venue_name": "Park Square Live Music & Coffee",
      #   "artist_id": 5,
      #   "artist_name": "Matt Quevedo",
      #   "artist_image_link": "https://images.unsplash.com/photo-1495223153807-b916f75de8c5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=334&q=80",
      #   "start_time": "2019-06-15T23:00:00.000Z"
      # }, {
      #   "venue_id": 3,
      #   "venue_name": "Park Square Live Music & Coffee",
      #   "artist_id": 6,
      #   "artist_name": "The Wild Sax Band",
      #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      #   "start_time": "2035-04-01T20:00:00.000Z"
      # }, {
      #   "venue_id": 3,
      #   "venue_name": "Park Square Live Music & Coffee",
      #   "artist_id": 6,
      #   "artist_name": "The Wild Sax Band",
      #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      #   "start_time": "2035-04-08T20:00:00.000Z"
      # }, {
      #   "venue_id": 3,
      #   "venue_name": "Park Square Live Music & Coffee",
      #   "artist_id": 6,
      #   "artist_name": "The Wild Sax Band",
      #   "artist_image_link": "https://images.unsplash.com/photo-1558369981-f9ca78462e61?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=794&q=80",
      #   "start_time": "2035-04-15T20:00:00.000Z"
      # }]
      return render_template('pages/shows.html', shows=data)

    @app.route('/shows/create', methods=['GET'])
    def create_shows():
      # renders form. do not touch.
      form = ShowForm()
      return render_template('forms/new_show.html', form=form)


    #  Create Show
    #  ----------------------------------------------------------------

    @app.route('/shows/create', methods=['GET','POST'])
    def create_show_submission():
      # called to create new shows in the db, upon submitting new show listing form
      # TODO: insert form data as a new Show record in the db, instead
      form = ShowForm()
      
      if form.validate_on_submit():
        venue_id = form.venue_id.data
        artist_id = form.artist_id.data
        start_time = form.start_time.data
        show = Show(venue_id=venue_id, artist_id=artist_id, start_time=start_time)
        db.session.add(show)
        db.session.commit()
        flash('Show was successfully listed!')
        return redirect(url_for('index')) 
        # on successful db insert, flash success
        # flash('Show was successfully listed!')
      # TODO: on unsuccessful db insert, flash an error instead.
      # e.g., flash('An error occurred. Show could not be listed.')
      # see: http://flask.pocoo.org/docs/1.0/patterns/flashing/
      if form.errors:
        flash(form.errors)
        return redirect(url_for('create_show_submission'))
      return render_template('pages/home.html')


    #  Error Handling
    #  ----------------------------------------------------------------

    @app.errorhandler(404)
    def not_found_error(error):
        return render_template('errors/404.html'), 404

    @app.errorhandler(500)
    def server_error(error):
        return render_template('errors/500.html'), 500


    if not app.debug:
        file_handler = FileHandler('error.log')
        file_handler.setFormatter(
            Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
        )
        app.logger.setLevel(logging.INFO)
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        app.logger.info('errors')








    return app

    #----------------------------------------------------------------------------#
    # Launch.
    #----------------------------------------------------------------------------#

    # Default port:
    # if __name__ == '__main__':
    #     app.run()

    # Or specify port manually:
    '''
    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        app.run(host='0.0.0.0', port=port)
'''

app = create_app('config')