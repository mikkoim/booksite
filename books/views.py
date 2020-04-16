from django.shortcuts import render
from .models import Bookmodel, Reviewmodel, Shelfmodel

from . import bookutil
from . import visualizations

def index(request):
    if Shelfmodel.objects.all().exists():
        shelf = Shelfmodel.objects.all()[0]

        reviewlist = [review for review in shelf.reviewmodel_set.order_by('-read_at')]
        booklist = [review.book.title for review in reviewlist]

        df = bookutil.reviewlist_to_df(reviewlist)
        
        script, div = visualizations.create_bokeh_plot(df)

        context = {'booklist': booklist,
                    'script': script,
                    'div': div}

    return render(request, 'books/index.html', context)

def refresh(request):
    context = {}
    if 'user_id' in request.GET and request.GET ['user_id'] != '':
        user_id = request.GET ['user_id']

        shelf = bookutil.get_read_shelf(str(user_id))

        # Shelf
        if not Shelfmodel.objects.filter(user_id=user_id):
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
        


        booklist = [review.book.title for review in shelf]
        context = {'booklist': booklist,
                    'user_id': user_id}
    
    return render(request, 'books/refresh.html', context)
