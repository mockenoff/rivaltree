import Ember from 'ember';

const equal = (params) => params[0] == params[1];

export default Ember.Helper.helper(equal);
