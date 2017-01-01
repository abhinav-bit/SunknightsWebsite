from django.db import models
from .diep_tank import DiepTank
from .points_info import PointsInfo, ClanUser
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .point_submission import BasicUserPointSubmission
from ..backgroundTask.webhook_spam import mastery_unlock
from .utility.little_things import MASTERY_TIER_OPTIONS,getMasteryRankByPoints


class Mastery(models.Model):

    tank = models.ForeignKey(DiepTank, on_delete=models.CASCADE)
    pointsinfo = models.ForeignKey(PointsInfo, on_delete=models.CASCADE, related_name='masteries')
    tier = models.PositiveSmallIntegerField(choices=MASTERY_TIER_OPTIONS)
    manager = models.ForeignKey(ClanUser)
    fromSubmission = models.BooleanField(default=True)
    points = models.PositiveSmallIntegerField(default=0)  # will be modified after save by receiver

    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.tank.name

    class Meta:
        ordering = ['tank']
        unique_together = ('tank', 'pointsinfo')


        # https://web.archive.org/web/20120715042306/http://codeblogging.net/blogs/1/14


@receiver(post_save, sender=Mastery)
def update_points_on_save(sender, instance, created=False, **kwargs):
    """This is an extremly lazy (not efficient) method to always keep currentpoints up to date -
    regardless if a submission was accepted, unaccapted, created, deleted, whatever.
    A better method would be to just add/subtract points on specific actions"""

    mastery = instance
    tier = mastery.tier
    points = 0

    if tier is 1:
        points = 5
    elif tier is 2:
        points = 15
    elif tier is 3:
        points = 30
    if (mastery.points != points) or created:
        mastery.points = points
        mastery.save()
        pointsupdater(mastery.pointsinfo)





def pointsupdater(pointsinfo):  # TODO add masteries points
    sumPoints = Mastery.objects.filter(pointsinfo=pointsinfo).filter(fromSubmission=True).aggregate(models.Sum('points'))['points__sum'] or 0.0#mastery points from google docs document should already be included in old points
    pointsinfo.masterypoints = sumPoints
    pointsinfo.save()


@receiver(post_delete, sender=Mastery)
def update_points_on_delete(sender, instance, **kwargs):
    pointsinfo = instance.pointsinfo
    pointsupdater(pointsinfo)



    # https://web.archive.org/web/20120715042306/http://codeblogging.net/blogs/1/14


@receiver(post_save, sender=BasicUserPointSubmission)
def update_submission_points_on_save(sender, instance, created=False, **kwargs):
    """This is an extremly lazy (not efficient) method to always keep currentpoints up to date -
    regardless if a submission was accepted, unaccapted, created, deleted, whatever.
    A better method would be to just add/subtract points on specific actions"""

    submission = instance
    tank = submission.tank
    tier = getMasteryRankByPoints(submission.score)
    pointsinfo = submission.pointsinfo
    manager = submission.manager

    if submission.accepted and tier > 0:  # check if another mastery can be granted
        try:
            mastery = Mastery.objects.get(tank=tank, pointsinfo=pointsinfo)
        except Mastery.DoesNotExist:
            mastery=Mastery.objects.create(tank=tank, pointsinfo=pointsinfo, tier=tier, manager=manager)
            mastery_unlock(mastery)
        else:
            if mastery.fromSubmission is False:
                mastery.fromSubmission = True
                mastery.save()

            if mastery.tier < tier:
                mastery.manager = manager
                mastery.fromSubmission = True
                mastery.tier = tier
                mastery.save()
                mastery_unlock(mastery)
