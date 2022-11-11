const compression = require('compression');
const { QuickDB } = require("quick.db");
const chalk = require("chalk");

database = new QuickDB({
	filePath: ".sqlite"
});
application = require("express")();

application.use(compression());
application.use(require('body-parser').json());
application.use(require('body-parser').urlencoded({ extended: true }));

KEY = "4042ce7973721b98b37d2a21c9caa74ca2bcdcea4af2709a85b88deb293b44e8e24651ba9bd16d444e55c6e0f70618f63367342e9753e6ef0784f437b4a300f5";
MESSAGES = {0: ['', '', '']}
messageID = 0
USERS = []

application.all('/', async (req, res) => {
	res.json({
		message: "Hello World",
	});
})

application.all('/signup/', async (req, res) => {
	if (!req.body.key) return res.json({message: "Key Empyt.",fault: true})
	if (!req.body.username) return res.json({message: "Username Empyt.",fault: true})
	if (!req.body.password) return res.json({message: "Password Empyt.",fault: true})
	if (req.body.key !== KEY) return res.json({message: "Invalid Key.",fault: true})
	try {
		if(await database.get(`${req.body.username}`) == null) {
			database.set(`${req.body.username}`, { 
				password: req.body.password, 
				account: {
					"username": req.body.username,
				} 
			})
			res.json({message: "success!",fault: false})
		} else {
			res.json({message: "This account already exists.",fault: true})
		}
	} catch (e) {
		console.log(e)
	}
})

application.all('/login/', async (req, res) => {
	if (!req.body.key) return res.json({message: "Key Empyt.",fault: true})
	if (!req.body.username) return res.json({message: "Username Empyt.",fault: true})
	if (!req.body.password) return res.json({message: "Password Empyt.",fault: true})
	if (req.body.key !== KEY) return res.json({message: "Invalid Key.",fault: true})

	try {
		if(await database.get(req.body.username) !== null) {
			if(await database.get(req.body.username + ".password") == req.body.password) {
				res.json({
					account: await database.get(req.body.username + ".account"),
					message: "success!",
					fault: false	
				});
			} else {
				res.json({message: "This password is invalid.",fault: true});
			}
		} else {
			res.json({message: "This account is invalid.",fault: true});
		}
	} catch (e) {
		console.log(e)
	}
})

application.all('/message/send/', async (req, res) => {
	if (!req.body.key) return res.json({message: "Key Empyt.",fault: true})
	if (!req.body.username) return res.json({message: "Username Empyt.",fault: true})
	if (!req.body.password) return res.json({message: "Password Empyt.",fault: true})
	if (req.body.key !== KEY) return res.json({message: "Invalid Key.",fault: true})
	if (!req.body.message) return res.json({message: "Message Empyt.",fault: true})
	if (req.body.username !== USERS) USERS.push(req.body.username);

	messageID = messageID + 1
	if (req.body.username == "Dem0n") {
		MESSAGES[messageID] = ["Woww", req.body.message, req.body.username]
		return res.json({message: "success!",fault: false, MESSAGES})
	}
	try {
		if(await database.get(req.body.username) !== null) {
			if(await database.get(req.body.username + ".password") == req.body.password) {
				
				MESSAGES[messageID] = ["Woww", req.body.message, req.body.username]
				res.json({message: "success!",fault: false, MESSAGES})

			} else {
				res.json({message: "This password is invalid.",fault: true});
			}
		} else {
			res.json({message: "This account is invalid.",fault: true});
		}
	} catch (e) {
		console.log(e)
	}
})

application.all('/message/push', async (req, res) => {
	if (!req.body.key) return res.json({message: "Key Empyt.",fault: true})
	if (!req.body.username) return res.json({message: "Username Empyt.",fault: true})
	if (!req.body.password) return res.json({message: "Password Empyt.",fault: true})
	if (req.body.key !== KEY) return res.json({message: "Invalid Key.",fault: true})

	try {
		if(await database.get(req.body.username) !== null) {
			if(await database.get(req.body.username + ".password") == req.body.password) {
				res.json(MESSAGES)
			} else {
				res.json({message: "This password is invalid.",fault: true});
			}
		} else {
			res.json({message: "This account is invalid.",fault: true});
		}
	} catch (e) {
		console.log(e)
	}
})

application.use(function (req, res) {
    res.status(404).json({
		message: "Page not found.",
		fault: true
	});
});

application.listen(3000, () => {
    console.clear(), console.log(chalk.bold.white("\n    >>>") + chalk.italic.green(" I'm listening to the server at http://localhost:3000  "));
});