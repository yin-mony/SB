from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.core.models import Badge


class Command(BaseCommand):
    help = "Seed test badges into `badges` table"

    def handle(self, *args, **options):
        rows = [
            ("逻辑学徒", "发起 1 个话题", "badge-scroll", '{"topics_created": 1}'),
            ("逻辑粉碎机", "发起 3 个话题", "badge-brain", '{"topics_created": 3}'),
            ("外星翻译官", "发起 5 个话题", "badge-rocket", '{"topics_created": 5}'),
            ("抬杠新秀", "发布 1 条观点", "badge-lightning", '{"debate_posts": 1}'),
            ("抬杠冠军", "发布 5 条观点", "badge-crown", '{"debate_posts": 5}'),
            ("深夜哲学家", "深夜发帖 1 次", "badge-flame", '{"late_night_posts": 1}'),
            ("码字见习生", "发布 1 篇文章", "badge-quill", '{"blog_posts": 1}'),
            ("码字狂魔", "发布 3 篇文章", "badge-medal", '{"blog_posts": 3}'),
            ("人气启动", "获得 1 个粉丝", "badge-heart", '{"followers": 1}'),
            ("众星捧月", "获得 5 个粉丝", "badge-star", '{"followers": 5}'),
            ("社交雷达", "关注 1 人", "badge-compass", '{"following": 1}'),
            ("甜蜜收割", "累计获赞 5", "badge-shield", '{"likes_total": 5}'),
        ]
        now = timezone.now()
        inserted = 0
        updated = 0
        for name, description, icon, condition_json in rows:
            obj = Badge.objects.filter(name=name).first()
            if not obj:
                Badge.objects.create(
                    name=name,
                    description=description,
                    icon=icon,
                    condition_json=condition_json,
                    created_at=now,
                )
                inserted += 1
                continue
            Badge.objects.filter(id=obj.id).update(description=description, icon=icon, condition_json=condition_json)
            updated += 1

        self.stdout.write(f"inserted={inserted} updated={updated} badges_count={Badge.objects.count()}")

