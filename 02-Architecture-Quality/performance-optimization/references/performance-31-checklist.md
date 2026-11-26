# قائمة تدقيق الأداء — 31 معيارًا

طبّق هذه القائمة كجرد أولي فقط. لكل معيار سجّل `مطبق` أو `غير مطبق` أو `يحتاج تحسين` أو `غير مناسب`، ثم اذكر الدليل، الأولوية، الأثر المتوقع، وطريقة القياس. لا تضف تقنية بلا دليل على ملاءمتها.

1. Skeleton Loading
2. WebP / AVIF
3. Duplicate API Calls
4. Debounce
5. Pagination
6. CDN
7. Background Job Queue
8. N+1 Queries
9. Brotli / Gzip
10. Redis Caching
11. Unused Dependencies
12. API Timeouts
13. AI Streaming
14. Optimistic UI
15. Lazy Loading
16. Parallel Requests
17. Database Indexes
18. OpenTelemetry
19. Server / Database Proximity
20. SSR / Static Generation
21. Third-Party Scripts
22. Code Splitting
23. Virtualization
24. Required Columns Only
25. Connection Pooling
26. Unnecessary Re-renders
27. Browser Caching
28. Load Balancing
29. Font Optimization
30. Real User Monitoring
31. Performance Testing

## طريقة التقييم

ابدأ بقراءة الكود والبنية وقياس خط أساس قبل التعديل. افحص الواجهة، network waterfall، server traces، database queries، bundle، cache headers، وقياسات الأجهزة والشبكات البطيئة حسب ما ينطبق. اربط كل معيار بمكان في الكود أو trace أو metric، ولا تعتبر غياب التقنية عيبًا بذاته.

بعد كل تغيير، قِس بالطريقة نفسها وفي الظروف نفسها. افصل التغييرات حتى يمكن عزو النتيجة. احتفظ بتحسين يتجاوز ضوضاء القياس ولا يكسر الوظيفة؛ أعد أو ارجع تحسينًا بلا تحسن قابل للقياس. سجّل أيضًا المحاولات التي تم التراجع عنها حتى لا يعيدها وكيل لاحقًا.

## صيغة التقرير المختصر

| # | المعيار | الحالة | الدليل الحالي | الأولوية | القياس قبل/بعد | القرار |
|---:|---|---|---|---|---|---|
| 1–31 | اسم المعيار | مطبق / غير مطبق / يحتاج تحسين / غير مناسب | ملف أو trace أو metric | عالية / متوسطة / منخفضة | رقم أو غير مقاس | نفذ / أجّل / لا تطبق |

## ضوابط

حافظ على الوظائف والتصميم والسلوك الحالي. اختبر desktop وmobile، والأجهزة البطيئة والشبكات الضعيفة عندما يكون ذلك مؤثرًا. لا تخلط performance testing مع security testing؛ اختبارات الحمل والأمن تحتاج نطاقًا وأدوات وتصريحًا مناسبًا.
