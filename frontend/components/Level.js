import React from 'react';
import Link from 'next/link';
import Router, { withRouter } from 'next/router';
import {Col, Card, CardBody, CardHeader, CardTitle, CardSubtitle, CardText, Progress, Input, Button, Form, FormGroup, Alert} from 'reactstrap';
import { getStageById, getQuestions, clearLevel } from '../services/data';

class Level extends React.Component {

  constructor(props) {
    super(props);
    this.state = {
      level: props.router.query.level,
      stageId: props.router.query.stageId,
      stageName: null,
      questions: [],
      currentQuestionIndex: null,
      userAnswer: "",
      answerState: null,
      streakCount: 0,
      previousCorrect: false,
      numAttempts: 0,
    }
  }

  componentDidMount() {
    let stage = getStageById(this.state.stageId);
    let questions = getQuestions(this.state.level, this.state.stageId).questions;
    this.setState({
      stageName: stage.name,
      questions: questions,
      currentQuestionIndex: 0
    });
  }

  onCheckQuestionBtnClick() {
    if(this.state.userAnswer == null || this.state.userAnswer == ""){
      this.setState({
        answerState: null,
        streakCount: 0,
        previousCorrect: false,
        numAttempts: this.state.numAttempts+1,
      })
    } else if(this.state.userAnswer == this.state.questions[this.state.currentQuestionIndex].answer){
      this.setState({
        answerState: true,
        numAttempts: this.state.numAttempts+1,
      });
    } else {
      this.setState({
        answerState: false,
        streakCount: 0,
        previousCorrect: false,
        numAttempts: this.state.numAttempts+1,
      });
    }
  }

  onNextQuestionBtnClick() {
    if(!this.state.answerState){
      return;
    }
    // if we only have 3 or less questions left in the questions array then fetch more questions from the service
    if(this.state.questions.length - this.currentQuestionIndex <= 3){
      let newQuestions = getQuestions(this.state.level, this.state.stageId);
      let questions = this.state.questions;
      questions = questions.concat(newQuestions);
      this.setState({questions: questions});
     }

    // update the streak count (a streak is number of questions user answers correct in a row)
    let currentStreakCount = this.state.streakCount+1;
    if( (this.state.previousCorrect || this.state.currentQuestionIndex == 0) && this.state.numAttempts <= 1 ){
      this.setState({streakCount: currentStreakCount});
    }

    // update `previousCorrect` if this question was done in a single attempt before moving to the next question
    if(this.state.numAttempts <= 1){
      this.setState({previousCorrect: true});
    }

    // increment the `currentQuestionIndex` by 1 to move to the next question
    this.setState({
      currentQuestionIndex: this.state.currentQuestionIndex+1,
      numAttempts: 0,
      answerState: null,
      userAnswer: "",
    });

    // mark the level as cleared if the required streak is completed. currently this is a static value of 8
    if(currentStreakCount >= 2){
      clearLevel(this.state.level, this.state.stageId);
      console.log("here it is");
    } else {
      console.log(this.state);
    }

  }

  handleAnswerChange(event) {
    this.setState({userAnswer: event.target.value.trim()});
  }

  getAnswerStateAlert() {
    if(this.state.answerState == false) {
      return <Alert color="danger">Wrong answer.</Alert>
    }
    else if(this.state.answerState == null || this.state.answerState == ""){
      return <Alert color="primary">Fill your answer in the textbox.</Alert>
    } else {
      return <Alert color="success">Correct answer.</Alert>
    }
  }

  render() {
    if(this.state.currentQuestionIndex == null){
      return <></>
    }
    return (
      <>
      <Col xs="12" sm="12" md="12" lg="12" xl="12"><h1>Level {this.state.level} ({this.state.stageName})</h1></Col>
      <Col xs="12" sm="12" md="12" lg="12" xl="12">
        <Card>
          <CardHeader>
            <Progress value={(this.state.streakCount/2)*100} color="success">{this.state.streakCount} in a row :)</Progress>
          </CardHeader>
          <CardBody>
              {this.getAnswerStateAlert()}
              <CardText>{ this.state.questions[this.state.currentQuestionIndex].text }</CardText>
            <Form>
              <FormGroup>
                <Input type="textarea" name="text" id="questionAnswer" value={this.state.userAnswer} onChange={this.handleAnswerChange.bind(this)} />
              </FormGroup>
              <FormGroup>
                <Button color="primary" size="lg" onClick={() => this.onCheckQuestionBtnClick()}>Check Answer</Button>{' '}
                <Button color="primary" size="lg" onClick={() => this.onNextQuestionBtnClick()}>Next Question</Button>
              </FormGroup>
              {this.state.streakCount >= 2 ?
                <FormGroup>
                  <Link href={`/stage?id=`+this.state.stageId}>
                    <Button color="success" size="lg" block>Go to Next Level :D</Button>
                  </Link>
                </FormGroup>
              : null}
            </Form>
          </CardBody>
        </Card>
      </Col>
      </>
    )
  }

}

export default withRouter(Level);