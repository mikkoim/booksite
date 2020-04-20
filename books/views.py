from django.shortcuts import render
from .models import Bookmodel, Reviewmodel, Shelfmodel

from . import bookutil
from . import visualizations

def index(request):

    user_id = request.session.get('user_id',-1)
    reviewlist = []
    script = []
    div = []
    

    # If user ID is given
    if 'user_id' in request.GET:
        if request.GET['user_id'] != '':
            user_id = request.GET['user_id']

            request.session['user_id'] = user_id
            request.session.modified = True
            
            refresh_shelf(user_id)

    if Shelfmodel.objects.filter(user_id=user_id).exists():

        shelf = Shelfmodel.objects.get(user_id=user_id)

        reviewlist = [review for review in shelf.reviewmodel_set.order_by('-read_at')]
        df = bookutil.reviewlist_to_df(reviewlist)
        
        script, div = visualizations.create_bokeh_plot(df)

    context = {'reviewlist': reviewlist,
                'user_id': user_id,
                'script': script,
                'div': div}

    return render(request, 'books/index.html', context)


def refresh_shelf(user_id):
    shelf = bookutil.get_read_shelf(str(user_id))

    # Shelf
    if not Shelfmodel.objects.filter(user_id=user_id).exists():
        shelf_mod = Shelfmodel.objects.create(name=shelf.name,
                                                user_id=user_id)
        shelf_mod.save()
    else:
        shelf_mod = Shelfmodel.objects.get(user_id=user_id)

        # Clear shelf
        for review_mod in shelf_mod.reviewmodel_set.all():
            review_mod.delete()


    # Reviews and books
    for review in shelf:

        # Book
        book = review.book
        if not Bookmodel.objects.filter(title=book.title).exists():

            book_mod = Bookmodel.objects.create(title=book.title,
                                                image_url=book.image_url,
                                                num_pages=book.num_pages,
                                                publication_year=book.publication_year,
                                                average_rating=book.average_rating,
                                                ratings_count=book.ratings_count,
                                                author=book.author)

            book_mod.save()
        else:
            book_mod = Bookmodel.objects.get(title=book.title)

        # Review
        review_mod = Reviewmodel.objects.create(book=book_mod,
                                            rating=review.rating,
                                            started_at=review.started_at,
                                            read_at=review.read_at)

        review_mod.shelf.add(shelf_mod)
        review_mod.save()

def refresh(request):
    context = {}
    return render(request, 'books/refresh.html', context)
