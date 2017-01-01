# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-01 19:28
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ClanUser',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('discord_id', models.PositiveIntegerField(default=0, unique=True)),
                ('discord_nickname', models.CharField(default='', max_length=50)),
                ('provider', models.CharField(default='Discord', max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('is_superuser', models.BooleanField(default=False)),
                ('avatar', models.CharField(default='', max_length=150)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BasicPointSubmission',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('accepted', models.BooleanField(default=False)),
                ('decided', models.BooleanField(default=False)),
                ('managerText', models.TextField(blank='', default='', max_length=200)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('points', models.DecimalField(db_index=True, decimal_places=2, default=0, max_digits=6)),
            ],
        ),
        migrations.CreateModel(
            name='ClanUserRoles',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('clan_user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='roles', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='DailyQuest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('task', models.TextField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='DiepGamemode',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('diep_isDeleted', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='DiepTank',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30, unique=True)),
                ('diep_isDeleted', models.BooleanField(default=False)),
                ('multiplier', models.DecimalField(decimal_places=2, default=1.0, max_digits=3)),
                ('tier', models.PositiveSmallIntegerField(choices=[(1, 'Tier 1'), (2, 'Tier 2'), (3, 'Tier 3'), (4, 'Tier 4')])),
            ],
            options={
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='DiepTankInheritance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('me', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='inheritance', to='sunknightsapp.DiepTank')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='sunknightsapp.DiepTank')),
            ],
        ),
        migrations.CreateModel(
            name='DiscordRole',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('discord_id', models.PositiveIntegerField(default=0, unique=True)),
                ('discord_color', models.IntegerField(default=0)),
                ('can_manage_points', models.BooleanField(default=False)),
                ('can_manage_wars', models.BooleanField(default=False)),
                ('discord_isDeleted', models.BooleanField(default=False)),
                ('guild_leader_role', models.BooleanField(default=False)),
                ('is_clan_guild', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='DiscordServer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('discord_id', models.PositiveIntegerField(unique=True)),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='GuildFight',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Not Finished'), (2, 'Team 1 won'), (3, 'Team 2 won'), (4, 'Draw')])),
                ('rules', models.PositiveSmallIntegerField(choices=[(1, 'No Rules'), (2, 'Only lvl 45tanks with each from a unique lvl 30 tank'), (3, 'Only unique lvl 45tanks'), (4, 'Only lvl 45tanks')], default=1)),
                ('number_of_players', models.PositiveIntegerField(default=6)),
                ('pointswinner', models.PositiveSmallIntegerField(default=10)),
                ('pointsloser', models.PositiveSmallIntegerField(default=5)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='manager', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='GuildFightParticipation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='participant', to='sunknightsapp.GuildFight')),
            ],
        ),
        migrations.CreateModel(
            name='Mastery',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tier', models.PositiveSmallIntegerField(choices=[(1, 'Tier 1'), (2, 'Tier 2'), (3, 'Tier 3')])),
                ('fromSubmission', models.BooleanField(default=True)),
                ('points', models.PositiveSmallIntegerField(default=0)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('manager', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['tank'],
            },
        ),
        migrations.CreateModel(
            name='PointsInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('oldpoints', models.DecimalField(decimal_places=2, default=0, max_digits=19)),
                ('currentpoints', models.DecimalField(decimal_places=2, default=0, max_digits=19)),
                ('masterypoints', models.DecimalField(db_index=True, decimal_places=2, default=0, max_digits=19)),
                ('totalpoints', models.DecimalField(db_index=True, decimal_places=2, default=0, max_digits=19)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tournament',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('description', models.TextField(max_length=500)),
                ('finished', models.BooleanField(default=False)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='TournamentFightConnector',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fight', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fight_connector', to='sunknightsapp.GuildFight')),
                ('tournament', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fight_connectors', to='sunknightsapp.Tournament')),
            ],
        ),
        migrations.CreateModel(
            name='BasicUserPointSubmission',
            fields=[
                ('basicpointsubmission_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sunknightsapp.BasicPointSubmission')),
                ('submitterText', models.TextField(default='', max_length=200)),
                ('proof', models.CharField(max_length=200, unique=True)),
                ('score', models.PositiveIntegerField(default=0)),
                ('gamemode', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sunknightsapp.DiepGamemode')),
                ('tank', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sunknightsapp.DiepTank')),
            ],
            bases=('sunknightsapp.basicpointsubmission',),
        ),
        migrations.CreateModel(
            name='OneOnOneFightSubmission',
            fields=[
                ('basicpointsubmission_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sunknightsapp.BasicPointSubmission')),
                ('proof', models.CharField(max_length=200, unique=True)),
                ('pointsloser', models.DecimalField(db_index=True, decimal_places=2, default=3, max_digits=6)),
                ('pointsinfoloser', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='loser', to='sunknightsapp.PointsInfo')),
            ],
            bases=('sunknightsapp.basicpointsubmission',),
        ),
        migrations.CreateModel(
            name='PointsManagerAction',
            fields=[
                ('basicpointsubmission_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sunknightsapp.BasicPointSubmission')),
            ],
            bases=('sunknightsapp.basicpointsubmission',),
        ),
        migrations.CreateModel(
            name='SunKnightsGuild',
            fields=[
                ('discordrole_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sunknightsapp.DiscordRole')),
            ],
            bases=('sunknightsapp.discordrole',),
        ),
        migrations.AddField(
            model_name='mastery',
            name='pointsinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='masteries', to='sunknightsapp.PointsInfo'),
        ),
        migrations.AddField(
            model_name='mastery',
            name='tank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sunknightsapp.DiepTank'),
        ),
        migrations.AddField(
            model_name='guildfightparticipation',
            name='guild',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guildfight_guild', to='sunknightsapp.DiscordRole'),
        ),
        migrations.AddField(
            model_name='guildfightparticipation',
            name='tank',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='fightparticipationtank', to='sunknightsapp.DiepTank'),
        ),
        migrations.AddField(
            model_name='guildfightparticipation',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='guildfight', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='guildfight',
            name='team1',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team1', to='sunknightsapp.DiscordRole'),
        ),
        migrations.AddField(
            model_name='guildfight',
            name='team2',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='team2', to='sunknightsapp.DiscordRole'),
        ),
        migrations.AddField(
            model_name='discordrole',
            name='discord_server',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sunknightsapp.DiscordServer'),
        ),
        migrations.AddField(
            model_name='clanuserroles',
            name='role',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sunknightsapp.DiscordRole'),
        ),
        migrations.AddField(
            model_name='basicpointsubmission',
            name='manager',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='basicpointsubmission',
            name='pointsinfo',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sunknightsapp.PointsInfo'),
        ),
        migrations.CreateModel(
            name='GuildFightPointsAction',
            fields=[
                ('pointsmanageraction_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='sunknightsapp.PointsManagerAction')),
            ],
            bases=('sunknightsapp.pointsmanageraction',),
        ),
        migrations.AlterUniqueTogether(
            name='tournamentfightconnector',
            unique_together=set([('tournament', 'fight')]),
        ),
        migrations.AlterUniqueTogether(
            name='mastery',
            unique_together=set([('tank', 'pointsinfo')]),
        ),
        migrations.AlterUniqueTogether(
            name='guildfightparticipation',
            unique_together=set([('fight', 'user')]),
        ),
        migrations.AlterUniqueTogether(
            name='dieptankinheritance',
            unique_together=set([('me', 'parent')]),
        ),
        migrations.AlterUniqueTogether(
            name='clanuserroles',
            unique_together=set([('clan_user', 'role')]),
        ),
        migrations.AddField(
            model_name='guildfightpointsaction',
            name='fightparticipation',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='sunknightsapp.GuildFightParticipation'),
        ),
    ]
