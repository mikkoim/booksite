from django.shortcuts import render
from django.http import HttpResponseRedirect
from .models import Bookmodel, Reviewmodel, Shelfmodel
from .forms import UserForm, ShelfForm

from . import bookutil
from . import visualizations

def index(request):

    # Set initial variables
    user_id = request.session.get('user_id',-1)
    shelfname = request.session.get('shelfname','read')

    shelf_list = bookutil.get_shelves_list(user_id)
    reviewlist = []
    script = []
    div = []
    

    # Build shelf dropdown form
    if request.method == 'POST':

        form = ShelfForm(shelf_list, request.POST)

        if form.is_valid():
            shelfname = form.cleaned_data['shelfname']

            # Refresh shelf
            if form.cleaned_data['refresh']=='True':
                print('\n\n\n REFRESSS\n\n\n')
                refresh_shelf(user_id, shelfname)  
            
            # Save shelfname to session
            request.session['shelfname'] = shelfname
            request.session.modified = True
    else: 
        form = ShelfForm(shelf_list)

    # Show shelf
    if Shelfmodel.objects.filter(user_id=user_id,
                                name=shelfname).exists():

        shelf = Shelfmodel.objects.get(user_id=user_id,
                                        name=shelfname)

        # Create table from shelf
        if shelfname == 'read':
            order = '-read_at'
        else:
            order = '-book__average_rating'
        reviewlist = [review for review in shelf.reviewmodel_set.order_by(order)]
        df = bookutil.reviewlist_to_df(reviewlist)
        
        # Create visualization
        script, div = visualizations.create_bokeh_plot(df)

    context = {'reviewlist': reviewlist,
                'form': form,
                'user_id': user_id,
                'shelfname': shelfname,
                'script': script,
                'div': div}

    return render(request, 'books/index.html', context)


def refresh_shelf(user_id, shelfname):
    shelf = bookutil.get_shelf(str(user_id), shelfname)

    #print('\n\n\n\n\n\nREFRESSHHHHHHHHHH\n\n\n\n\n\n')

    # Shelf
    if not Shelfmodel.objects.filter(user_id=user_id,
                                    name=shelfname).exists():
        shelf_mod = Shelfmodel.objects.create(name=shelf.name,
                                                user_id=user_id)
        shelf_mod.save()
    else:
        shelf_mod = Shelfmodel.objects.get(user_id=user_id,
                                            name=shelfname)

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

def set_user(request):

    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            
            user_id = str(form.cleaned_data['user_id'])
            #shelflist = bookutil.get_shelves_list(user_id)
            #for shelfname in shelflist:
            #    refresh_shelf(user_id, shelfname)  

            # save user id to session
            request.session['user_id'] = user_id
            request.session.modified = True

            return HttpResponseRedirect('/')
    else: 
        form = UserForm()
    context = {'form': form}
    return render(request, 'books/set_user.html', context)
