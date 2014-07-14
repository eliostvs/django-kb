from django.contrib.auth.models import User

from knowledge.base import choices
from knowledge.models import Article, Category
from model_mommy.recipe import foreign_key, Recipe, related

person = Recipe(User)

private_draft_article = Recipe(Article,
                               title='Title Private and Draft',
                               content='Content Private and Draft',
                               visibility=choices.VisibilityChoice.Private,
                               publish_state=choices.PublishChoice.Draft,
                               created_by=foreign_key(person))

private_published_article = Recipe(Article,
                                   title='Title Private and Published',
                                   content='Content Private and Published',
                                   visibility=choices.VisibilityChoice.Private,
                                   publish_state=choices.PublishChoice.Published,
                                   created_by=foreign_key(person))

public_draft_article = Recipe(Article,
                              title='Title Public and Draft',
                              content='Content Public and Draft',
                              visibility=choices.VisibilityChoice.Public,
                              publish_state=choices.PublishChoice.Draft,
                              created_by=foreign_key(person))

public_published_article = Recipe('Article',
                                  title='Title Public and Published',
                                  content='Content Public and Published',
                                  visibility=choices.VisibilityChoice.Public,
                                  publish_state=choices.PublishChoice.Published,
                                  created_by=foreign_key(person))


public_category = Recipe(Category,
                         name='Public Category Name',
                         description='Public Category Description')

private_category = Recipe(Category,
                          name='Private Category Name',
                          description='Private Category Description',
                          visibility=choices.VisibilityChoice.Private)

category_without_articles = Recipe(Category,
                                   name='Category Without Articles')

public_category_with_articles = Recipe(Category,
                                       name='Public Category Name',
                                       description='Public Category Description',
                                       articles=related('private_draft_article',
                                                        'private_published_article',
                                                        'public_draft_article',
                                                        'public_published_article'))
private_category_with_articles = Recipe(Category,
                                        name='Private Category Name',
                                        description='Private Category Description',
                                        visibility=choices.VisibilityChoice.Private,
                                        articles=related('private_draft_article',
                                                         'private_published_article',
                                                         'public_draft_article',
                                                         'public_published_article'))
