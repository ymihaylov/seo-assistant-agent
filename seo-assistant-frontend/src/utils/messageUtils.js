export const transformApiMessage = (msg) => {
  if (msg.role === 'user') {
    return {
      id: msg.id,
      type: 'user',
      content: msg.message_content,
      timestamp: new Date(msg.created_at)
    };
  } else {
    return {
      id: msg.id,
      type: 'agent',
      content: {
        title: msg.suggested_page_title,
        content: msg.suggested_page_content,
        titleTag: msg.suggested_title_tag,
        metaDescription: msg.suggested_meta_description,
        metaKeywords: msg.suggested_meta_keywords
      },
      timestamp: new Date(msg.created_at)
    };
  }
};

export const createUserMessage = (userMessageData) => ({
  id: userMessageData.id,
  type: 'user',
  content: userMessageData.message_content,
  timestamp: new Date(userMessageData.created_at)
});

export const createAgentMessage = (agentMessageData) => ({
  id: agentMessageData.id,
  type: 'agent',
  content: {
    title: agentMessageData.suggested_page_title,
    content: agentMessageData.suggested_page_content,
    titleTag: agentMessageData.suggested_title_tag,
    metaDescription: agentMessageData.suggested_meta_description,
    metaKeywords: agentMessageData.suggested_meta_keywords
  },
  timestamp: new Date(agentMessageData.created_at)
});
