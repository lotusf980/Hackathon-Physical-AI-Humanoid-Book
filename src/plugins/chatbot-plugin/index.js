module.exports = function chatbotPlugin(context, options) {
  return {
    name: 'chatbot-plugin',

    getClientModules() {
      return [require.resolve('./ChatbotInjector')];
    },
  };
};