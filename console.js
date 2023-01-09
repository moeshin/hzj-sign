await (async () => {
    const url = localStorage.uri;
    const token = localStorage.token || sessionStorage.token;
    console.log('url', url);
    console.log('token', token);
    const request = p => fetch(url + p, {
        method: 'POST',
        headers: {
            "content-type": "application/x-www-form-urlencoded",
        },
        body: new URLSearchParams({token}).toString(),
    }).then(r => r.json()).then(d => d.data);
    const studentId = (JSON.parse(sessionStorage.PersonalData)
        || await request('/mobile/getData'))['user']['student']['id'];
    console.log('studentId', studentId);
    const {internshipId} = await request('/mobile/plan/internship/find-stu-current-or-not-start-internship');
    console.log('internshipId', internshipId);
    console.log(JSON.stringify({
        sign: {
            url,
            token,
            studentId,
            internshipId,
        },
    }, null, 2));
})();
