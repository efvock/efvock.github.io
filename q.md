---
layout: default
title: 質問一覧
---

<h1>質問一覧</h1>

<ul>
  {% for question in site.questions %}
    <li>
      <a href="{{ question.url }}">{{ question.title }}</a>
    </li>
  {% endfor %}
</ul>
