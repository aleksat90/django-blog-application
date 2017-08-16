# from django.db import models
# from django.utils import timezone
# from django.core.urlresolvers import reverse
# # Create your models here.
#
# class Post(models.Model):
#     author = models.ForeignKey('auth.User')
#     title = models.CharField(max_length=200)
#     text = models.TextField() #ne znamo koliko ce biti dugacak tekst
#     created_date = models.DateTimeField(default=timezone.now)
#     published_date = models.DateTimeField(blank=True,null=True) #moze da bude prazno ili da bude null
#
#     #Kada kliknes publish, uzece vreme u tom trenutku i snimiti u published_date
#     def publish(self):
#         self.published_date = timezone.now()
#         self.save()
#
#     #negde cemo imati listu dozvoljenih ili ne dozvoljenih komentara, odobrene, cemo filtrirati
#     def approve_comments(self):
#         return self.comments.filter(approved_comment = True)
#
#     def get_absoulute_url(self):
#         #posto kreiras post idi na postdetiail gde je pk parametar ustvari pk(primary key)
#         return reverse('post_detail',kwargs={'pk':self.pk})
#
#     def __str__(self):
#         return self.title
#
#
# class Comment(models.Model):
#     #ovo ce svaki comment da poveze sa Postom
#     post = models.ForeignKey('blog.Post',related_name='comments')
#     author = models.CharField(max_length='200')
#     text = models.TextField()
#     create_date = models.DateTimeField(default=timezone.now)
#     #mora da bude istp kao i u return self.comments.filter(approved_comment = True)
#     approved_comment = models.BooleanField(default= False)
#
#     def approve(self):
#         self.approved_comment = True
#         self.save()
#
#     def get_absoulute_url(self):
#         #U urls.py ces pronaci gde te post_list vodi
#         return reverse('post_list')
#
#     def __str__(self):
#         return self.text

#posto neko kreira post ili comment gde ce ga to odvesti


from django.db import models
from django.utils import timezone
from django.core.urlresolvers import reverse


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def approve_comments(self):
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("post_detail",kwargs={'pk':self.pk})


    def __str__(self):
        return self.title



class Comment(models.Model):
    post = models.ForeignKey('blog.Post', related_name='comments')
    author = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text
