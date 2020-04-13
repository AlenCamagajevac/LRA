import { ImageSourcePropType } from 'react-native';

export class Article {

  constructor(title,description, content, image,date, author, likes, comments) {
  }

  static howToEatHealthy() {
    return new Article(
      'How To Eat Healthy',
      '10 useful Tips',
      'There\'s a lot of advice out there on how to eat healthy, and if we\'re being honest, it can sometimes feel like too much to think about. Especially when you\'re hungry. Remember when you were a kid and eating was as simple as open, chew, enjoy? Yes, those were simpler times. Now, knowing how to eat healthy doesn\'t seem quite as straightforward. Between the diet fads, gourmet trends, and a rotating roster of superfoods, eating well has gotten, well, complicated.',
      require('../assets/image-article-background-1.jpg'),
      '19 Sep, 2018',
      Profile.markVolter(),
      [
        Like.byMarkVolter(),
        Like.byHubertFranck(),
      ],
      [
        Comment.byHubertFranck(),
        Comment.byHubertFranck(),
        Comment.byHubertFranck(),
      ],
    );
  }

  static whyWorkoutImportant() {
    return new Article(
      'Why Is The Workout Important?',
      'Some Tips',
      'There\'s a lot of advice out there on how to eat healthy, and if we\'re being honest, it can sometimes feel like too much to think about. Especially when you\'re hungry. Remember when you were a kid and eating was as simple as open, chew, enjoy? Yes, those were simpler times. Now, knowing how to eat healthy doesn\'t seem quite as straightforward. Between the diet fads, gourmet trends, and a rotating roster of superfoods, eating well has gotten, well, complicated.',
      require('../assets/image-article-background-2.jpg'),
      '19 Sep, 2018',
      Profile.hubertFranck(),
      [
        Like.byMarkVolter(),
        Like.byHubertFranck(),
      ],
      [
        Comment.byHubertFranck(),
        Comment.byHubertFranck(),
        Comment.byHubertFranck(),
      ],
    );
  }

  static morningWorkouts() {
    return new Article(
      '5 Rules Of Morning Workouts',
      '5 Useful Exercises',
      'There\'s a lot of advice out there on how to eat healthy, and if we\'re being honest, it can sometimes feel like too much to think about. Especially when you\'re hungry. Remember when you were a kid and eating was as simple as open, chew, enjoy? Yes, those were simpler times. Now, knowing how to eat healthy doesn\'t seem quite as straightforward. Between the diet fads, gourmet trends, and a rotating roster of superfoods, eating well has gotten, well, complicated.',
      require('../assets/image-article-background-3.jpg'),
      '19 Sep, 2018',
      Profile.markVolter(),
      [
        Like.byMarkVolter(),
        Like.byHubertFranck(),
      ],
      [
        Comment.byHubertFranck(),
        Comment.byHubertFranck(),
        Comment.byHubertFranck(),
      ],
    );
  }
}

export class Like {

  constructor(author) {

  }

  static byMarkVolter() {
    return new Like(
      Profile.markVolter(),
    );
  }

  static byHubertFranck() {
    return new Like(
      Profile.hubertFranck(),
    );
  }
}

export class Comment {

  constructor(text, date, author, comments, likes) {
  }

  static byHubertFranck() {
    return new Comment(
      'This very useful information for me Thanks for your article!',
      'Today 11:10 am',
      Profile.hubertFranck(),
      [
        Comment.byMarkVolter(),
      ],
      [
        Like.byMarkVolter(),
      ],
    );
  }

  static byMarkVolter() {
    return new Comment(
      'Thanks!',
      'Today 11:10 am',
      Profile.hubertFranck(),
      [],
      [],
    );
  }

}

export class Profile {

  constructor(firstName, lastName, photo) {
  }

  get fullName() {
    return `${this.firstName} ${this.lastName}`;
  }

  static markVolter() {
    let mark = new Profile(
      'Mark',
      'Volter',
      require('../assets/image-profile.jpg'),
    );
    console.log("mark", mark);
  }

  static hubertFranck() {
    return new Profile(
      'Hubert',
      'Franck',
      require('../assets/image-profile.jpg'),
    );
  }
}