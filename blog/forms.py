from django import forms

from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            "title",
            "slug",
            "country",
            "city_or_region",
            "hero_image",
            "short_description",
            "full_description",
        ]
        widgets = {
            "short_description": forms.Textarea(attrs={"rows": 4}),
            "full_description": forms.Textarea(attrs={"rows": 12}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for name, field in self.fields.items():
            css_class = "form-control form-control-lg"
            if name == "hero_image":
                css_class = "form-control form-control-lg"
            if name in {"short_description", "full_description"}:
                field.widget.attrs.update({"class": css_class})
            else:
                field.widget.attrs.update({"class": css_class})
