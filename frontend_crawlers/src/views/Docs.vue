<template>
    <b-container>
        <b-row class="card-deck justify-content-md-center">
            <b-col md="8">
                <h1
                    dir="ltr"
                    style="line-height:1.38;margin-top:20pt;margin-bottom:6pt;"
                >
                    <span
                        style="font-size:20pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >Как пользоваться Linkedin API&nbsp;</span
                    >
                </h1>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                >
                    <a
                        href="https://linkedin.devlabsco.com/api-docs/#/"
                        style="text-decoration:none;"
                        ><span
                            style="font-size:11pt;font-family:Arial;color:#1155cc;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:underline;-webkit-text-decoration-skip:none;text-decoration-skip-ink:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                            >https://linkedin.devlabsco.com/api-docs/</span
                        ></a
                    >
                </p>
                <h2
                    dir="ltr"
                    style="line-height:1.38;margin-top:18pt;margin-bottom:6pt;"
                >
                    <span
                        style="font-size:16pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >Регистрация и логи</span
                    >
                </h2>
                <p><br /></p>
                <ol
                    style="margin-top:0;margin-bottom:0;padding-inline-start:48px;"
                >
                    <li
                        aria-level="1"
                        dir="ltr"
                        style="list-style-type:decimal;font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;"
                    >
                        <p
                            dir="ltr"
                            style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                        >
                            <span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >Завести аккаунт в нашем сервисе (&nbsp;</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >/user/create&nbsp;</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >)</span
                            >
                        </p>
                    </li>
                    <li
                        aria-level="1"
                        dir="ltr"
                        style="list-style-type:decimal;font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;"
                    >
                        <p
                            dir="ltr"
                            style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                        >
                            <span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >Авторизоваться (&nbsp;</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >/auth</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >&nbsp;) - получить на выходе token который во
                                всех запросах используется для авторизации</span
                            >
                        </p>
                    </li>
                    <li
                        aria-level="1"
                        dir="ltr"
                        style="list-style-type:decimal;font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;"
                    >
                        <p
                            dir="ltr"
                            style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                        >
                            <span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >Добавить аккаунт(ы) Linkedin, чтобы с их
                                помощью можно было выполнять все предоставляемые
                                сервисом действия (в API этот параметр
                                называется credentials_id). Для этого есть 2
                                способа:</span
                            >
                        </p>
                    </li>
                </ol>
                <p><br /></p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-left: 36pt;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >2.1 (</span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >не рекомендованный</span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >) добавить логин и пароль от своего аккаунта</span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        ><br /></span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >POST /account</span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        ><br /></span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        ><span class="Apple-tab-span" style="white-space:pre;"
                            >&nbsp; &nbsp;&nbsp;</span
                        ></span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        ><span class="Apple-tab-span" style="white-space:pre;"
                            >&nbsp; &nbsp;&nbsp;</span
                        ></span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >{</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-left: 108pt;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp; &quot;input_data&quot;: {</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-left: 108pt;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp; &nbsp; &quot;login&quot;:
                        &quot;linkedinlogin@gmail.com&quot;,</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-left: 108pt;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp; &nbsp; &quot;password&quot;:
                        &quot;mypass1234&quot;</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-left: 108pt;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp; }</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-left: 108pt;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp;}</span
                    >
                </p>
                <p><br /></p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-left: 36pt;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >2.2 (</span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >рекомендованный</span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >) добавить cookie с linkedin&nbsp;</span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        ><br /></span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >POST /account</span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        ><br /></span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        ><span class="Apple-tab-span" style="white-space:pre;"
                            >&nbsp; &nbsp;&nbsp;</span
                        ></span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        ><span class="Apple-tab-span" style="white-space:pre;"
                            >&nbsp; &nbsp;&nbsp;</span
                        ></span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >{</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-left: 108pt;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp; &quot;input_data&quot;: {</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-left: 108pt;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp; &nbsp; &quot;login&quot;:
                        &quot;linkedinlogin@gmail.com&quot;,</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-left: 108pt;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp; &nbsp; &quot;li_at&quot;:
                        &quot;A12edwadcwe4rfwecfrtg45gre&quot;,</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-left: 108pt;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp; }</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-left: 108pt;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp;}</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >Чтобы узнать свои li_at cookie надо сделать
                        следующее:&nbsp;</span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        ><br /></span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >в Google chrome скачать расширение&nbsp;</span
                    ><a
                        href="https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg/related?hl=ru"
                        style="text-decoration:none;"
                        ><span
                            style="font-size:11pt;font-family:Arial;color:#1155cc;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:underline;-webkit-text-decoration-skip:none;text-decoration-skip-ink:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                            >https://chrome.google.com/webstore/detail/editthiscookie/fngmhnnpilhplaeedifhccceomclgfbg/related?hl=ru</span
                        ></a
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp;(или любое другое, позволяющее смотреть Ваши
                        cookie), зайти на Ваш аккаунт Linkedin и вызвать это
                        расширение,</span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        ><br /></span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        ><span
                            style="border:none;display:inline-block;overflow:hidden;width:487px;height:294px;"
                            ><img
                                src="https://lh6.googleusercontent.com/CqpHggP57DQmir0HUNCN0G_hLn89DqNExOqjqvHmu4cRmpQzlFg1xcY7cs2m2seEdXp0o_PsORyZjrwX_2TqMrfpvFDyPbSN63eR43uMPme-HbKnnzZ7Irid6yuFXVFFxAVfg0pb"
                                width="487"
                                height="294"/></span
                    ></span>
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >найти поле&nbsp;</span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >li_at&nbsp;</span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >и скопировать его&nbsp;</span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >значение</span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >:&nbsp;</span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        ><br /></span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        ><span
                            style="border:none;display:inline-block;overflow:hidden;width:576px;height:361px;"
                            ><img
                                src="https://lh6.googleusercontent.com/jO8JYfhyuJ0Ur9FZ0dCNWn75-1WNz5NuuUuQv73h4-U3K5p0lTQ5wo52a3kZI2RNGFhghwrX_t9sharLMbs3t5WcFJ03USDSJtGVqGoYg-a12RWFUkKwOX4TIWp37KMIFyYf5ZLL"
                                width="576"
                                height="361"/></span
                    ></span>
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >Когда аккаунт создан, из ответа сервера надо сохранить
                        себе&nbsp;</span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >credentials_id&nbsp;</span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >этого аккаунта (его надо указывать для всех
                        запросов)</span
                    >
                </p>
                <ol
                    start="4"
                    style="margin-top:0;margin-bottom:0;padding-inline-start:48px;"
                >
                    <li
                        aria-level="1"
                        dir="ltr"
                        style="list-style-type:decimal;font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;"
                    >
                        <p
                            dir="ltr"
                            style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                        >
                            <span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >Можно получить все свои аккаунты и
                                их&nbsp;</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >credentials_id</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >&nbsp;через GET /accounts</span
                            >
                        </p>
                    </li>
                    <li
                        aria-level="1"
                        dir="ltr"
                        style="list-style-type:decimal;font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;"
                    >
                        <p
                            dir="ltr"
                            style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                        >
                            <span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >Все действия в сервисе логируются - можно их
                                посмотреть через POST /actions упорядоченные по
                                дате, либо посмотреть последнее выполненное
                                действие в системе через POST /action,
                                результаты запросов будут в поле result_data,
                                если указать в input_data action, то можно
                                получить действия только конкретного типа</span
                            >
                        </p>
                    </li>
                </ol>
                <p><br /></p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >action_codes: {</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp; &nbsp; &nbsp; &nbsp; linkedin_check_reply:
                        1,</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp; &nbsp; &nbsp; &nbsp; linkedin_connect: 2,</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp; &nbsp; &nbsp; &nbsp; linkedin_send_message:
                        3,</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp; &nbsp; &nbsp; &nbsp; linkedin_check_accept:
                        4,</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp; &nbsp; &nbsp; &nbsp; linkedin_search: 5,</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp; &nbsp; &nbsp; &nbsp; linkedin_parse_profile:
                        6,</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp; &nbsp; &nbsp; &nbsp; linkedin_visit_profile:
                        7,</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp; &nbsp; &nbsp; &nbsp; linkedin_search_sn:
                        8,</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp; &nbsp; &nbsp; &nbsp; linkedin_parse_profile_sn:
                        9,</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp; &nbsp; &nbsp; &nbsp; linkedin_post_parsing:
                        10,</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp; &nbsp; &nbsp; &nbsp; linkedin_search_scribe:
                        11,</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp; &nbsp; &nbsp; &nbsp; linkedin_search_scribe_sn:
                        12,</span
                    >
                </p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp; &nbsp; },</span
                    >
                </p>
                <p><br /></p>
                <h2
                    dir="ltr"
                    style="line-height:1.38;margin-top:18pt;margin-bottom:6pt;"
                >
                    <span
                        style="font-size:16pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >Возможные действия с Linkedin API</span
                    >
                </h2>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >Важно!</span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >&nbsp;Перед началом использования&nbsp;</span
                    ><a
                        href="https://filtpod.com/new-linkedin-connection-request-limits-2021/"
                        style="text-decoration:none;"
                        ><span
                            style="font-size:11pt;font-family:Arial;color:#1155cc;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:underline;-webkit-text-decoration-skip:none;text-decoration-skip-ink:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                            >ознакомьтесь&nbsp;</span
                        ></a
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >с ЛИМИТАМИ Linkedin на количество посещаемых страниц \
                        профайлов и проч.</span
                    >
                </p>
                <ol
                    style="margin-top:0;margin-bottom:0;padding-inline-start:48px;"
                >
                    <li
                        aria-level="1"
                        dir="ltr"
                        style="list-style-type:decimal;font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;"
                    >
                        <p
                            dir="ltr"
                            style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                        >
                            <span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >/search</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >На вход: ссылка на Linkedin search
                                (например&nbsp;</span
                            ><a
                                href="https://www.linkedin.com/sales/search/people?doFetchHeroCard=false&functionIncluded=11%2C21&geoIncluded=91000005&industryIncluded=15&keywords=covid-19&logHistory=false&page=2&preserveScrollPosition=false&profileLanguage=en&rsLogId=894145129&searchSessionId=XD5tNQp5QK2LK4yS%2ByoRLQ%3D%3D"
                                style="text-decoration:none;"
                                ><span
                                    style="font-size:11pt;font-family:Arial;color:#1155cc;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:underline;-webkit-text-decoration-skip:none;text-decoration-skip-ink:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                    >https://www.linkedin.com/search/people?doFetchHeroCard=false&amp;functionIncluded=11%2C21&amp;geoIncluded=91000005&amp;industryIncluded=15&amp;keywords=covid-19&amp;logHistory=false&amp;page=2&amp;preserveScrollPosition=false&amp;profileLanguage=en&amp;rsLogId=894145129&amp;searchSessionId=XD5tNQp5QK2LK4yS%2ByoRLQ%3D%3D</span
                                ></a
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >&nbsp;), количество страниц для сбора
                                информации</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >На выходе: список всех найденных людей с
                                указанием их имени, фамилии, должности,
                                компании</span
                            >
                        </p>
                    </li>
                    <li
                        aria-level="1"
                        dir="ltr"
                        style="list-style-type:decimal;font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;"
                    >
                        <p
                            dir="ltr"
                            style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                        >
                            <span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >/scribe</span
                            >
                        </p>
                    </li>
                </ol>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-left: 36pt;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >На вход: ссылка на Linkedin profile&nbsp;</span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        ><br /></span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >На выходе: вся найденная информация по юзеру (если он
                        виден для аккаунта) - имя, фамилия, должность, компания,
                        образование, местонахождение, сайт компании</span
                    >
                </p>
                <ol
                    start="3"
                    style="margin-top:0;margin-bottom:0;padding-inline-start:48px;"
                >
                    <li
                        aria-level="1"
                        dir="ltr"
                        style="list-style-type:decimal;font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;"
                    >
                        <p
                            dir="ltr"
                            style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                        >
                            <span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >/search/scribe</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >На вход: ссылка на Linkedin search
                                (например&nbsp;</span
                            ><a
                                href="https://www.linkedin.com/sales/search/people?doFetchHeroCard=false&functionIncluded=11%2C21&geoIncluded=91000005&industryIncluded=15&keywords=covid-19&logHistory=false&page=2&preserveScrollPosition=false&profileLanguage=en&rsLogId=894145129&searchSessionId=XD5tNQp5QK2LK4yS%2ByoRLQ%3D%3D"
                                style="text-decoration:none;"
                                ><span
                                    style="font-size:11pt;font-family:Arial;color:#1155cc;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:underline;-webkit-text-decoration-skip:none;text-decoration-skip-ink:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                    >https://www.linkedin.com/sales/people?doFetchHeroCard=false&amp;functionIncluded=11%2C21&amp;geoIncluded=91000005&amp;industryIncluded=15&amp;keywords=covid-19&amp;logHistory=false&amp;page=2&amp;preserveScrollPosition=false&amp;profileLanguage=en&amp;rsLogId=894145129&amp;searchSessionId=XD5tNQp5QK2LK4yS%2ByoRLQ%3D%3D</span
                                ></a
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >&nbsp;)</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >На выходе: список всех найденных людей с
                                указанием их имя, фамилия, должность, компания,
                                образование, местонахождение, сайт
                                компании</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >Отличие от /search - более полная информация
                                находится.&nbsp;</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >Важно!</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >&nbsp;Метод работает ~110-130 сек на найденный
                                профайл, то есть результаты его выполнения надо
                                ждать и брать из логов /actions</span
                            >
                        </p>
                    </li>
                    <li
                        aria-level="1"
                        dir="ltr"
                        style="list-style-type:decimal;font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;"
                    >
                        <p
                            dir="ltr"
                            style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                        >
                            <span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >/message</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >На вход: ссылка на Linkedin profile и сообщение
                                для этого юзера</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >На выходе: результат - сообщение отправлено \
                                не отправлено</span
                            >
                        </p>
                    </li>
                    <li
                        aria-level="1"
                        dir="ltr"
                        style="list-style-type:decimal;font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;"
                    >
                        <p
                            dir="ltr"
                            style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                        >
                            <span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >/message/check</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >На вход: ссылка на Linkedin profile</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >На выходе: результат - юзер ответил \ не
                                ответил</span
                            >
                        </p>
                    </li>
                    <li
                        aria-level="1"
                        dir="ltr"
                        style="list-style-type:decimal;font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;"
                    >
                        <p
                            dir="ltr"
                            style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                        >
                            <span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >/connect</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >На вход: ссылка на Linkedin profile и сообщение
                                для этого юзера</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >На выходе: результат - запрос на добавление
                                отправлен \ не отправлен</span
                            >
                        </p>
                    </li>
                    <li
                        aria-level="1"
                        dir="ltr"
                        style="list-style-type:decimal;font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;"
                    >
                        <p
                            dir="ltr"
                            style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                        >
                            <span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >/connect/check</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >На вход: ссылка на Linkedin profile</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >На выходе: результат - юзер находится в списке
                                контактов или нет</span
                            >
                        </p>
                    </li>
                    <li
                        aria-level="1"
                        dir="ltr"
                        style="list-style-type:decimal;font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;"
                    >
                        <p
                            dir="ltr"
                            style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                        >
                            <span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >/profile/visit</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >На вход: ссылка на Linkedin profile</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >На выходе: результат - посещён профайл юзера
                                или нет</span
                            >
                        </p>
                    </li>
                    <li
                        aria-level="1"
                        dir="ltr"
                        style="list-style-type:decimal;font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;"
                    >
                        <p
                            dir="ltr"
                            style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                        >
                            <span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >/post/engagement</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >На вход: ссылка на Linkedin post</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >На выходе: результат - список тех, кто лайкнул
                                и прокомментировал пост + основная информация о
                                самом посте</span
                            >
                        </p>
                    </li>
                </ol>
                <p><br /></p>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >Linkedin Sales Navigator</span
                    >
                </p>
                <ol
                    start="10"
                    style="margin-top:0;margin-bottom:0;padding-inline-start:48px;"
                >
                    <li
                        aria-level="1"
                        dir="ltr"
                        style="list-style-type:decimal;font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;"
                    >
                        <p
                            dir="ltr"
                            style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                        >
                            <span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >/sn/search</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >На вход: ссылка на Linkedin search
                                (например&nbsp;</span
                            ><a
                                href="https://www.linkedin.com/sales/search/people?doFetchHeroCard=false&functionIncluded=11%2C21&geoIncluded=91000005&industryIncluded=15&keywords=covid-19&logHistory=false&page=2&preserveScrollPosition=false&profileLanguage=en&rsLogId=894145129&searchSessionId=XD5tNQp5QK2LK4yS%2ByoRLQ%3D%3D"
                                style="text-decoration:none;"
                                ><span
                                    style="font-size:11pt;font-family:Arial;color:#1155cc;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:underline;-webkit-text-decoration-skip:none;text-decoration-skip-ink:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                    >https://www.linkedin.com/sales/search/people?doFetchHeroCard=false&amp;functionIncluded=11%2C21&amp;geoIncluded=91000005&amp;industryIncluded=15&amp;keywords=covid-19&amp;logHistory=false&amp;page=2&amp;preserveScrollPosition=false&amp;profileLanguage=en&amp;rsLogId=894145129&amp;searchSessionId=XD5tNQp5QK2LK4yS%2ByoRLQ%3D%3D</span
                                ></a
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >&nbsp;), количество страниц для сбора
                                информации</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >На выходе: список всех найденных людей с
                                указанием их имени, фамилии, должности,
                                компании</span
                            >
                        </p>
                    </li>
                    <li
                        aria-level="1"
                        dir="ltr"
                        style="list-style-type:decimal;font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;"
                    >
                        <p
                            dir="ltr"
                            style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                        >
                            <span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >/sn/scribe</span
                            >
                        </p>
                    </li>
                </ol>
                <p
                    dir="ltr"
                    style="line-height:1.38;margin-left: 36pt;margin-top:0pt;margin-bottom:0pt;"
                >
                    <span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >На вход: ссылка на Linkedin profile&nbsp;</span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        ><br /></span
                    ><span
                        style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                        >На выходе: вся найденная информация по юзеру (если он
                        виден для аккаунта) - имя, фамилия, должность, компания,
                        образование, местонахождение, сайт компании, сайты
                        профайла, имейлы, твиттер и другая контактная
                        информация</span
                    >
                </p>
                <ol
                    start="12"
                    style="margin-top:0;margin-bottom:0;padding-inline-start:48px;"
                >
                    <li
                        aria-level="1"
                        dir="ltr"
                        style="list-style-type:decimal;font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;"
                    >
                        <p
                            dir="ltr"
                            style="line-height:1.38;margin-top:0pt;margin-bottom:0pt;"
                        >
                            <span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >/sn/search/scribe</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >На вход: ссылка на Linkedin search
                                (например&nbsp;</span
                            ><a
                                href="https://www.linkedin.com/sales/search/people?doFetchHeroCard=false&functionIncluded=11%2C21&geoIncluded=91000005&industryIncluded=15&keywords=covid-19&logHistory=false&page=2&preserveScrollPosition=false&profileLanguage=en&rsLogId=894145129&searchSessionId=XD5tNQp5QK2LK4yS%2ByoRLQ%3D%3D"
                                style="text-decoration:none;"
                                ><span
                                    style="font-size:11pt;font-family:Arial;color:#1155cc;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:underline;-webkit-text-decoration-skip:none;text-decoration-skip-ink:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                    >https://www.linkedin.com/sales/search/people?doFetchHeroCard=false&amp;functionIncluded=11%2C21&amp;geoIncluded=91000005&amp;industryIncluded=15&amp;keywords=covid-19&amp;logHistory=false&amp;page=2&amp;preserveScrollPosition=false&amp;profileLanguage=en&amp;rsLogId=894145129&amp;searchSessionId=XD5tNQp5QK2LK4yS%2ByoRLQ%3D%3D</span
                                ></a
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >&nbsp;)</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >На выходе: список всех найденных людей с
                                указанием их имя, фамилия, должность, компания,
                                образование, местонахождение, сайт компании,
                                сайты профайла, имейлы, твиттер и другая
                                контактная информация</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >Отличие от /sn/search - более полная информация
                                находится.&nbsp;</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                ><br /></span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:700;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >Важно!</span
                            ><span
                                style="font-size:11pt;font-family:Arial;color:#000000;background-color:transparent;font-weight:400;font-style:normal;font-variant:normal;text-decoration:none;vertical-align:baseline;white-space:pre;white-space:pre-wrap;"
                                >&nbsp;Метод работает ~110-130 сек на найденный
                                профайл, то есть результаты его выполнения надо
                                ждать и брать из логов /actions</span
                            >
                        </p>
                    </li>
                </ol>
            </b-col>
        </b-row>
    </b-container>
</template>
