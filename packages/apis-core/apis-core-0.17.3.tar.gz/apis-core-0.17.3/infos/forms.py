# generated by appcreator
from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit,  Layout, Fieldset, Div, MultiField, HTML
from crispy_forms.bootstrap import Accordion, AccordionGroup
from . models import AboutTheProject, TeamMember, ProjectInst


class ProjectInstFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ProjectInstFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'id',
                'name',
                css_id="basic_search_fields"
                ),
            Accordion(
                AccordionGroup(
                    'More',
                    'website',
                    css_id="more"
                    ),
                )
            )


class ProjectInstForm(forms.ModelForm):
    class Meta:
        model = ProjectInst
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(ProjectInstForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class TeamMemberFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(TeamMemberFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'id',
                'name',
                css_id="basic_search_fields"
                ),
            Accordion(
                AccordionGroup(
                    'More',
                    'website',
                    'role',
                    css_id="more"
                    ),
                )
            )


class TeamMemberForm(forms.ModelForm):
    class Meta:
        model = TeamMember
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(TeamMemberForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)


class AboutTheProjectFilterFormHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(AboutTheProjectFilterFormHelper, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.form_class = 'genericFilterForm'
        self.form_method = 'GET'
        self.helper.form_tag = False
        self.add_input(Submit('Filter', 'Search'))
        self.layout = Layout(
            Fieldset(
                'Basic search options',
                'id',
                'description',
                css_id="basic_search_fields"
                ),
            Accordion(
                AccordionGroup(
                    'Authors',
                    'author',
                    css_id="more"
                    ),
                )
            )


class AboutTheProjectForm(forms.ModelForm):
    class Meta:
        model = AboutTheProject
        fields = "__all__"

    def __init__(self, *args, **kwargs):
        super(AboutTheProjectForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-3'
        self.helper.field_class = 'col-md-9'
        self.helper.add_input(Submit('submit', 'save'),)
