StandardCharsets = luajava.bindClass("java.nio.charset.StandardCharsets")
Class = luajava.bindClass("java.lang.Class")
JCasUtil = luajava.bindClass("org.apache.uima.fit.util.JCasUtil")
TopicUtils = luajava.bindClass("org.texttechnologylab.DockerUnifiedUIMAInterface.lua.DUUILuaUtils")
ArrayList = luajava.bindClass("java.util.ArrayList")

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

    print("Process text")
    local texts = nil
    local docText = inputCas:getDocumentText()
    local docLen = #docText
    -- FIXME: Temp test: Using whole text array as one input
    if docText and docLen > 0 then
        local texts_array = {}
        texts_array[1] = {
            text = docText,
            begin = 0,
            ['end'] = docLen
        }

        texts = {
            texts = texts_array,
            config = {
                model_name = parameters["text_model_name"],
            }
        }
    end

    print("Process Images")
    local images = nil
    local image_collection = JCasUtil:select(inputCas, Image)
    local image_collection_size = image_collection:size()
    if image_collection and image_collection_size > 0 then
        local images_array = {}
        local number_of_images = 1

        for i = 0, image_collection_size - 1 do
            local image = image_collection:get(i)
            images_array[number_of_images] = {
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
            }
        }
    end

    print("Process videos")
    local videos = nil
    local video_collection = JCasUtil:select(inputCas, Video)
    local video_collection_size = video_collection:size()
    if video_collection and video_collection_size > 0 then
        local videos_array = {}
        local number_of_videos = 1

        for i = 0, video_collection_size - 1 do
            local video = video_collection:get(i)
            videos_array[number_of_videos] = {
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
            }
        }
    end

    print("Process audios")
    local audios = nil
    local audio_collection = JCasUtil:select(inputCas, Audio)
    local audio_collection_size = audio_collection:size()
    if audio_collection and audio_collection_size > 0 then
        local audios_array = {}
        local number_of_audios = 1

        for i = 0, audio_collection_size - 1 do
            local audio = audio_collection:get(i)
            audios_array[i] = {
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
            }
        }
    end

    local request = {
        images = images,
        audios = audios,
        videos = videos,
        texts = texts,
        doc_lang = doc_lang,
        doc_len = doc_len
    }

    print(json.encode(request))

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