from wtforms import (Field, Form, StringField, validators, IntegerField,
                     RadioField, DateTimeField)
from wtforms.validators import ValidationError
from .db import POST_TEXT_MAX_LENGTH, TAG_MAX_LENGTH


class TagListField(Field):

    def _value(self):
        if self.data:
            return ', '.join(self.data)
        else:
            return ''

    def process_formdata(self, valuelist):
        if valuelist:
            self.data = [tag.strip() for tag in valuelist[0].split(',')]
        else:
            self.data = []

    def post_validate(self, form, validation_stopped):
        super().post_validate(form, validation_stopped)
        if not self.data:
            return
        for tag in self.data:
            if not tag.isalnum():
                raise ValidationError('tag is not alphanumeric')
            if len(tag) > TAG_MAX_LENGTH:
                raise ValidationError('tag cannot be longer than {}'.format(
                                      TAG_MAX_LENGTH))


tags_field = TagListField('tags', [validators.Length(max=255)])
order_field = RadioField('ordering', choices=[('asc', ''), ('desc', '')],
                         default='desc')


def isalnum(form, field):
    if not field.data.isalnum():
        raise ValidationError('value not is alphanumeric')


class CreateUserForm(Form):
    username = StringField('username', [validators.required(),
                                        validators.Length(max=30),
                                        isalnum])


class CreatePostForm(Form):
    user_id = IntegerField('user id', [validators.required()])
    title = StringField('title', [validators.required(),
                                  validators.Length(max=255)])
    text = StringField('text', [validators.Length(max=POST_TEXT_MAX_LENGTH)])
    tags = tags_field


class UserPostForm(Form):
    order = order_field
    tags = tags_field


class PostListForm(Form):
    tags = tags_field
    begin = DateTimeField('date_begin ')
    end = DateTimeField('date_end ')
    order = order_field
    title = StringField('title', [validators.Length(max=255)])
