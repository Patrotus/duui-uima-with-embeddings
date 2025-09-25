StandardCharsets = luajava.bindClass("java.nio.charset.StandardCharsets")
Class = luajava.bindClass("java.lang.Class")
JCasUtil = luajava.bindClass("org.apache.uima.fit.util.JCasUtil")
TopicUtils = luajava.bindClass("org.texttechnologylab.DockerUnifiedUIMAInterface.lua.DUUILuaUtils")

-- Types used in embeddings
Image = luajava.bindClass("org.texttechnologylab.annotation.type.Image")
Video = luajava.bindClass("org.texttechnologylab.annotation.type.Video")
Audio = luajava.bindClass("org.texttechnologylab.annotation.type.Audio")

-- TODO: Very unsure on how to add support for the per modality model config to this process
-- Converting to cas
function serialize(inputCas, outputStream, parameters)
    print("Start Lua serialization for embeddings")

    local doc_lang = inputCas:getDocumentLanguage()
    local doc_len = TopicUtils:getDocumentTextLength(inputCas)

    -- TODO: Im still a little bit confused whether the current implementation is even remotly correct

    local texts = nil
    local texts_array = {}
    local number_of_texts = 1
    local texts_in = luajava.newInstance("java.util.ArrayList", JCasUtil:select(inputCas, Text)):listIterator()
    while texts_in:hasNext() do
        local text = texts_in:next()
        texts_array[number_of_texts] {
            text = text:getText(),
            begin = text:getBegin(),
            ['end'] = text:getBegin(),
        }
        number_of_texts = number_of_texts + 1
    end
    texts = {
        texts = texts_array,
        config = {
            model_name = parameters["text_model_name"], -- TODO: I dont think this is correct
            model_params = {} -- TODO: Not supported yet
        }
    }


    local images = nil
    local images_array = {}
    local number_of_images = 1
    local images_in = luajava.newInstance("java.util.ArrayList", JCasUtil:select(inputCas, Image)):listIterator()
    while images_in:hasNext() do
        local image = images_in:next()
        images_array[number_of_images] {
            src = image:getSrc(),
            height = image:getHeight(),
            width = image:getWidth(),
            begin = image:getBegin(),
            ['end'] = image:getEnd()
        }
        number_of_images = number_of_images + 1
    end
    images = {
        images = images_array,
        config = {
            model_name = parameters["image_model_name"], -- TODO: I dont think this is correct
            model_params = {} -- TODO: Not supported yet
        }
    }

    local videos = nil
    local videos_array = {}
    local number_of_videos = 1
    local class = Class:forName("org.texttechnologylab.annotation.type.Video")
    local videos_in = JCasUtil:select(inputCas, class):iterator()
    while videos_in:hasNext() do
        local video = videos_in:next()
        videos_array[number_of_videos] {
            src = video:getSrc(),
            length = video:getLength(),
            fps = video:getFps(),
            begin = video:getBegin(),
            ['end'] = video:getEnd()
        }
        number_of_videos = number_of_videos + 1
    end
    videos = {
        videos = videos_array,
        config = {
            model_name = parameters["video_model_name"], -- TODO: I dont think this is correct
            model_params = {} -- TODO: Not supported yet
        }
    }

    local audios = nil
    local audios_array = {}
    local number_of_audios = 1
    local audio_in = JCasUtil:select(inputCas, Audio):iterator()
    while audio_in:hasNext() do
        local audio = audio_in:next()
        audios_array[number_of_audios] {
            src = audio:getSrc(),
            begin = audio:getBegin(),
            ['end'] = audio:getEnd()
        }
        number_of_audios = number_of_audios + 1
    end
    audios = {
        audios = audios_array,
        config = {
            model_name = parameters["audio_model_name"], -- TODO: I dont think this is correct
            model_params = {} -- TODO: Not supported yet
        }
    }

    local request = {
        images = images,
        audios = audios,
        videos = videos,
        texts = texts,
        doc_lang = doc_lang,
        doc_len = doc_len
    }

    outputStream:write(json.encode(request))
end

-- Converting back to cas
function deserialize(inputCas, inputStream)
    print("Start deserialize for embeddings")

    local inputString = luajava.newInstance("java.lang.String", inputStream:readAllBytes(), StandardCharsets.UTF_8)
    local response = json.decode(inputString)
    print(response)

    if response['errors'] ~= nil then
        local errors = response['errors']
        for _, error in ipairs(errors) do
            local warning = luajava.newInstance("org.texttechnologylab.annotation.AnnotationComment", inputCas)
            warning:setKey("error")
            warning:setValue(error)
            warning:addToIndexes()
        end
    end

    -- TODO: MetaData supplier

    if response['text_embeddings'] ~= nil then
        for i, embedding in ipairs(response['text_embeddings']) do
            local embed_anno = luajava.newInstance("org.texttechnologylab.annotation.embeddings.TextEmbedding", inputCas)

            local embed_fs = luajava.newInstance("org.apache.uima.jcas.cas.FloatArray", inputCas, #embedding.embedding)
            for j, value in ipairs(embedding.embedding) do
                embed_fs:set(j - 1, value)
            end

            embed_anno:setEmbedding(embed_fs)

            local shape_fs = luajava.newInstance("org.apache.uima.jcas.cas.IntegerArray", inputCas, #embedding.shape)
            for j, value in ipairs(embedding.shape) do
                shape_fs:set(j - 1, value)
            end
            embed_anno:setShape(shape_fs)

            embed_anno:addToIndexes()
        end
    end

    if response['image_embeddings'] ~= nil then
        for i, embedding in ipairs(response['image_embeddings']) do
            local embed_anno = luajava.newInstance("org.texttechnologylab.annotation.embeddings.ImageEmbedding", inputCas)

            local embed_fs = luajava.newInstance("org.apache.uima.jcas.cas.FloatArray", inputCas, #embedding.embedding)
            for j, value in ipairs(embedding.embedding) do
                embed_fs:set(j - 1, value)
            end

            embed_anno:setEmbedding(embed_fs)

            local shape_fs = luajava.newInstance("org.apache.uima.jcas.cas.IntegerArray", inputCas, #embedding.shape)
            for j, value in ipairs(embedding.shape) do
                shape_fs:set(j - 1, value)
            end
            embed_anno:setShape(shape_fs)

            embed_anno:addToIndexes()
        end
    end

    if response['video_embeddings'] ~= nil then
        for i, embedding in ipairs(response['video_embeddings']) do
            local embed_anno = luajava.newInstance("org.texttechnologylab.annotation.embeddings.VideoEmbedding", inputCas)

            local embed_fs = luajava.newInstance("org.apache.uima.jcas.cas.FloatArray", inputCas, #embedding.embedding)
            for j, value in ipairs(embedding.embedding) do
                embed_fs:set(j - 1, value)
            end

            embed_anno:setEmbedding(embed_fs)

            local shape_fs = luajava.newInstance("org.apache.uima.jcas.cas.IntegerArray", inputCas, #embedding.shape)
            for j, value in ipairs(embedding.shape) do
                shape_fs:set(j - 1, value)
            end
            embed_anno:setShape(shape_fs)

            embed_anno:addToIndexes()
        end
    end

    if response['audio_embeddings'] ~= nil then
        for i, embedding in ipairs(response['audio_embeddings']) do
            local embed_anno = luajava.newInstance("org.texttechnologylab.annotation.embeddings.AudioEmbedding", inputCas)

            local embed_fs = luajava.newInstance("org.apache.uima.jcas.cas.FloatArray", inputCas, #embedding.embedding)
            for j, value in ipairs(embedding.embedding) do
                embed_fs:set(j - 1, value)
            end

            embed_anno:setEmbedding(embed_fs)

            local shape_fs = luajava.newInstance("org.apache.uima.jcas.cas.IntegerArray", inputCas, #embedding.shape)
            for j, value in ipairs(embedding.shape) do
                shape_fs:set(j - 1, value)
            end
            embed_anno:setShape(shape_fs)

            embed_anno:addToIndexes()
        end
    end
end