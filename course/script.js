const tincan = new TinCan({
  recordStores: [{
    endpoint: "http://localhost:8080/xapi/",
    username: "my_key",
    password: "my_secret",
    allowFail: false
  }]
});

function sendStatement() {
  tincan.sendStatement({
    actor: {
      mbox: "mailto:test@example.com",
      name: "Test User",
      objectType: "Agent"
    },
    verb: {
      id: "http://adlnet.gov/expapi/verbs/completed",
      display: { "en-US": "completed" }
    },
    object: {
      id: "http://example.com/activities/test-activity",
      definition: {
        name: { "en-US": "Local Test Activity" }
      }
    }
  }, function (results, statement) {
    if (results[0].err !== null) {
      console.error("xAPI error:", results[0].err);
    } else {
      console.log("xAPI sent:", statement);
      const text = results[0].xhr.responseText;
      console.log("xAPI response:", text ? JSON.parse(text) : results[0].xhr.status);
    }
  });
}