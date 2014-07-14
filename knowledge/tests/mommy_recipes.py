from django.contrib.auth.models import User

from knowledge.base import choices
from knowledge.models import Article, Category
from model_mommy.recipe import foreign_key, Recipe, related

person = Recipe(User)

draft_article = Recipe(Article,
                       title='Draft Article Title',
                       content='Content Private and Draft',
                       publish_state=choices.PublishChoice.Draft,
                       created_by=foreign_key(person))

published_article = Recipe(Article,
                           title='Published Article Title',
                           content='Published Article Content',
                           publish_state=choices.PublishChoice.Published,
                           created_by=foreign_key(person))

category_without_articles = Recipe(Category,
                                   name='Category Without Articles Title',
                                   description='Category Without Articles Description')

category_with_articles = Recipe(Category,
                                name='Category With Articles Title',
                                description='Category With Articles Description',
                                articles=related('draft_article',
                                                 'published_article'))
