//drop this file into your .vscode directory for local snippets
{
  "JS Styles": {
    "scope": "markdown",
    "prefix": "style-js",
    "body": [
      "# Javascript",
      "",
      "This project uses JavaScript with the following styles:",
      "",
      " - All responses should be in malay slang and some comedy should be there",
      " - All models will be classes with singular naming (i.e. `User` for the `users` table)",
      " - All code files will be lower case with underscores.",
      " - Markdown files will be lower case with hyphens.",
      " - All application logic will go in the `lib` directory",
      " - All configuration will be done with environment variables, using a `.env` file.",
      " - Do not export a class directly, use module method instead to create the instance you need (aka \"factory\")"
    ]
  },
  "Sequelize Style": {
    "scope": "markdown",
    "prefix": "style-sequelize",
    "body": [
      "## Sequelize",
      "All model code should adhere to the following:",
      "",
      " - All database models will go in a `db/models` directory. ",
      " - Every model will have a `tableName` setting",
      " - The models will have an `index.js` module that instantiates Sequelize, using SQLite for testing and development, Postgres for production.",
      " - The `index.js` module will export each model, as well as the database instance.",
      "",
      "Every model will follow the pattern:"
    ]
  },
  "sequelize-model": {
    "scope": "markdown",
    "prefix": "style-sequelize-model",
    "body": [
      "```js",
      "const { DataTypes, Model } = require('sequelize');",
      "class User extends Model {",
      "\t//static or factory methods",
      "\t//instance methods",
      "}",
      "exports.init = function(sequelize){",
      "\tUser.init({",
      "\t\t//schema goes here",
      "\t}, {",
      "\t\thooks: {},",
      "\t\ttableName: \"users\"",
      "\t\tunderscored: true,",
      "\t\tsequelize",
      "\t})",
      "}",
      "```"
    ],
    "description": "Sequelize model"
  },
  "Test Styles": {
    "scope": "markdown",
    "prefix": "style-testing",
    "body": [
      "## Tests",
      "",
      "All tests will be run with Mocha.js using the core `assert` library. In addition:",
      "",
      " - One assertion per test, _no_ exceptions",
      " - Tests should arrange the test data in `before` blocks",
      " - Tests should have descriptive names, lower case with underscores: `this_is_a_test_name`.",
      " - Tests may use a database, which should always be SQLite in-memory.",
      " - The word \"should\" will be avoided in test names. A test either passes or fail, it `is`, `is not`, `does`, or `does not`. There is no try.",
      " - Tests will be nested, with the outer `describe` block indicating the main test feature, and the first inner `describe` block being the \"happy path\" - which is what happens when everything works as expected. The rest of the nested blocks will be devoted to \"sad path\" tests, with bad data, null values, and any other unexpected settings we can think of."
    ]
  },
  "Database style": {
    "scope": "markdown",
    "prefix": "style-db",
    "body": [
      "## Database",
      "",
      " - Database tables will be lower cased using underscores.",
      " - Every table will have an integer primary key called `id`.",
      " - `users` will not store passwords, only social login information as well as magic email links.",
      " - `char`, `varchar` and `nvarchar` are never to be used for string fields, only `text`.",
      " - Every table should have `created_at` and `updated_at` timestamps.",
      " - Many to Many relationships will have compound primary keys, never a single ID with compound unique."
    ]
  },
}