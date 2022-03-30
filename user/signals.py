from django.contrib.auth.models import User,Group,Permission

from django.db.models.signals import post_save
from django.dispatch import receiver
from user.models import Profile




@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        try:
            Profile.objects.create(user=instance)
            instance.groups.add(Group.objects.get(name = 'Default'))
            
        except:
            Group.objects.get_or_create(name='Default')
            instance.groups.add(Group.objects.get(name = 'Default'))
            # permission = Permission.objects.get(codename='change_user')
            # user.user_permissions.add(permission)
            # POST SAVE GROUP UPDATE DEFAULT PERM 
            
            
       