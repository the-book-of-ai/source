---
title: "How is hardware reshaping LLM design?"
channel: "Julia Turc"
channel_id: "UCMUy_WsUIYbM_hKR9drb9dA"
published: 2026-03-03
url: "https://www.youtube.com/watch?v=BSzhrZOp2x8"
language: en
caption_source: manual
method: youtubegpt
---

**How is hardware reshaping LLM design?**
(by Julia Turc — full transcript)

[00:00] One quadrillion floating point operations per second, or 1000 TFLOPs per second. That's the peak compute throughput of an NVIDIA H100 GPU. In theory, this should enable a traditional large language model with 8 billion parameters to generate up to 62,000 tokens per second. But somehow, even the fastest inference engines are stuck at 200 tokens per second.

[00:26] Clearly we're leaving a lot of compute on the table, so what's going on? This problem can be traced way back. For decades, Moore's Law kept doubling transistor density and implicitly raw compute. Memory, however, has been improving a lot more slowly. This imbalance became known as the memory wall. Around 2019, when AI model sizes exploded, the memory wall became a bottleneck for LLM inference.

[00:52] In this video, we'll see why that's the case and what the industry is doing about it. We'll look at the engineering optimizations behind serving large language models and new modeling techniques like diffusion, which are fighting the memory bottleneck. This video is sponsored by Inception, a company building diffusion based large language models and the infrastructure to serve them. You can think of an AI model as a computational graph where the nodes are operations, mostly matrix multiplications, and the edges are the operands.

[01:23] It's basically an algorithm that can be executed by a GPU processor. The secret sauce is in the model weights or parameters, which are learned during training. They're real valued matrices, usually stacked in layers. In this diagram, there are four layers, but normally they're in the hundreds. So the weights need to be stored somewhere. GPUs typically come with their own on-chip memory.

[01:48] This is static RAM or SRAM. It's fast but expensive to manufacture and takes a lot of physical space, which is why there's only so much of it. NVIDIA's H100 GPU has a bit over 50 megabytes of SRAM. That's not nearly enough for state-of-the-art LLMs. Open weight models go up to hundreds of gigabytes of storage and proprietary ones must be even larger.

[02:14] To support this demand, GPUs come with yet another level of memory placed near the processor, but not on the same chip. It's called high bandwidth memory or HBM. This is typically what people refer to when they say "GPU memory". Unlike SRAM, it uses a stacked die architecture that trades some speed for much greater capacity.

[02:37] An H100 comes with 80 gigabytes, much more suitable for storing the model weights. Granted, that's still not enough for state-of-the-art LLMs, but we'll pretend to be working with an 8 billion parameter model that fits comfortably. So from the HBM, the weights can now be streamed to the processor on demand. Say we get a user query, which we'll serve with a traditional auto-regressive LLM that generates output tokens one by one.

[03:06] Conceptually, the model operates layer by layer. For each layer, the corresponding weights are streamed from HBM into on-chip memory. For each operation within this layer, the operands make their way into the processor registers. The processor executes the operations and produces the output activations for that layer. When it runs out of space, the on-chip memory discards the cached weights to make room for the next set of weights.

[03:32] And the cycle repeats until the forward pass is completed. For auto regressive LLMs in particular, the result of a forward pass is a single next token prediction. In practice, model weights are copied in smaller chunks than entire layers, but layers are just easier to visualize. The important takeaway is that for every single token generated, the entire model, all billions of parameters, must complete this journey from the HBM to the processor.

[04:02] Throughout the video, I'll refer to this journey as a "model stream" or "model copy". Just remember, it's not a one-time atomic transfer. It's a continuous pipeline of bytes being copied. Today, the biggest performance bottleneck is specifically the data transfer between the HBM and on-chip memory. The rate of this transfer is what we call memory bandwidth. NVIDIA's H100 comes with a bit over 3.2 terabytes per second, which sounds plenty at first.

[04:32] In theory, even for a model of hundreds of gigabytes, we should be able to transfer it in less than a second. However, a single model transfer serves a single forward pass, and, in an auto-regressive LLM, a single output token. So an average size response of 1000 tokens requires 1000 full model streams. With this perspective, the latency we saw earlier is less surprising.

[05:00] An 8 billion model roughly takes 16 gigabytes of storage. With a memory bandwidth of 3.2 terabytes per second, we can afford to make exactly 200 transfers in a second. Assuming a negligible GPU runtime, that's a throughput of 200 tokens per second. This shows that model inference is heavily bottlenecked by memory bandwidth. My initial rough math showed that the GPU processor at its peak could handle hundreds of times more operations than this.

[05:31] Yet it's sitting idle, waiting for parameters to arrive. Now there are two things we could do about it. Option one, just wait for NVIDIA to improve memory bandwidth, but that's not very high agency. Option two is to reconsider the LLM inference algorithms to take better advantage of the available resources. To help us reason how an algorithm relates to the hardware utilization, we can use an established framework called the roofline model.

[06:00] As we'll see soon, it literally looks like the roofline of a house. It was introduced back in 2009. At the time it was developed specifically to reason about the gap between memory and compute on multi-core CPUs, a problem that turned out to be the defining hardware tension of the next 15 years. Today, the roofline model is particularly relevant for gauging the efficiency of LLM inference on GPUs.

[06:27] The X axis corresponds to a quantity called arithmetic intensity, measured in FLOPs per byte. It shows how much useful work the processor performs for each byte of data transferred from the main memory. Increasing arithmetic intensity is equivalent to amortizing the inevitable cost of memory access. I like to think of it in terms of personal travel.

[06:51] Whenever I fly from the US to Europe, there's an inevitable cost and time and money. But what is under my control is the duration of the trip. So if I stay for a single day, then it's a very expensive trip, but if I stay for a couple of weeks, then the cost is starting to be worth it. The Y axis measures the performance or compute rate in FLOPs per second. Basically, how many operations are executed per unit of time.

[07:19] The relationship between X and Y is linear. Y equals X times the memory bandwidth. In other words, performance equals arithmetic intensity times memory bandwidth. It's easy to verify if we write down the units. FLOPs per byte times bytes per second gives us FLOPs per second. Another way to think of it is that memory bandwidth is the slope of the performance line.

[07:45] Now performance can't grow to infinity. It's capped by the capabilities of the accelerator. As we saw earlier, the H100 peaks at a thousand TFLOPs per second. On this plot, we'll work with an A6000 GPU instead, following the paper where I took the benchmarks from. With this hard ceiling, we now have a roofline model, which enables us to reason how well an LLM inference algorithm is utilizing the available resources.

[08:14] If it falls to the left of the ridge point, the algorithm is memory bound. What caps its performance is the slope of this line, which is the memory bandwidth. In contrast, the region to the right of the ridge point is compute bound, since the limiting factor is the processor speed. This is the better place to be since the ceiling is higher. Overall, auto-regressive language models are memory bound.

[08:38] That was also the case for the models we discussed earlier, since their latency of 200 tokens per second is way under what an unconstrained GPU processor can deliver. But there's a nuance to this generally true statement. The nuance comes from the fact that LLM inference is actually a two-staged procedure. Stage one processes the text prompt into real valued embedding vectors. This is called prefill.

[09:03] Stage two generates one token at a time conditioned on the previous ones. This is called decode. From a performance point of view, this distinction is meaningful because the two stages fall into different regions of the roofline. Decode is memory bound and prefill is compute bound. The root cause of this discrepancy is the fact that, during prefill, all the prompt tokens are readily available.

[09:30] And thanks to the design of the Transformer architecture, they can all be processed simultaneously. Let's assume the prompt has three tokens. With a single forward pass through the model, and therefore a single model stream, we manage to process all of them. So during prefill, the ratio of tokens to model streams is three to one. This arithmetic intensity grows linearly with the sequence length.

[09:55] So for typical prompt lengths of hundreds or thousands of tokens, prefill easily crosses the ridge point. In contrast, during the decode stage, we need three separate forward passes in order to output three tokens. The ratio now is three tokens to three model streams. In other words, the arithmetic intensity is three times lower than prompt processing, and it doesn't change for longer responses.

[10:22] That's why LLM inference engines put a lot of thought into optimizing the decoding step, which is the bottleneck. You might be familiar with vLLM, SGLang or TensorRT. All these frameworks increase the arithmetic intensity of LLM inference with smart engineering hacks. When the inference algorithm itself limits parallelism for a single query, the most obvious fix is to serve multiple queries in parallel.

[10:49] That's known as batching. An inference server, which is a software component that exposes an API, receives requests with text prompts. It groups them into batches and then ships them off to the GPU. Decoding still happens iteratively one step at a time, but a single forward pass through the model is now extending all responses by an output token. The good news is that it's very easy to modify the computational graph to support batching.

[11:18] Most operations multiply a weight matrix W by an activation x. Without batching, x is a vector. With batching, x is a matrix with one column per query. Now storing a larger x in the on-chip memory does put some pressure on its capacity. But crucially, the really expensive part, which is streaming the model weights from the HBM, still only happens once.

[11:44] From an arithmetic intensity point of view, the numerator increases while the denominator stays constant. This pulls the inference algorithm upwards on the roofline. When implemented naively, batching comes with an opportunity cost. Some responses are longer than others. A binary yes or no question requires fewer iterations than an AI slop article, yet it takes up space in the batch until all instances are complete.

[12:13] That's why most inference engines today do continuous batching, also called iteration level scheduling. That means the batch is reconfigured after every iteration, so finalized instances are immediately swapped out for a new query. This way, there are no instances sitting idle in the batch and no bubbles in the pipeline. On the next iteration, all the members in the batch are updated with an extra output token and the cycle repeats.

[12:41] So batching involves some overhead, but it's worth it because it increases arithmetic intensity. How far can we push it though? Can we choose the batch size in a way that maximizes the GPU utilization? At first glance, it might seem that the limiting factor is just the size of the activations X. But there's another hidden memory cost that we haven't discussed yet. Remember, auto regressive models make predictions based on the past.

[13:09] So to compute the next token, we need to cache activations from the previously generated tokens. This is called the KV cache. K stands for keys, V stands for values. These are activations specific to the Transformer architecture. The KV cache holds an entry for every previously generated token in the batch. Because of its size, it must be stored in the HBM.

[13:34] During a forward pass, the relevant keys and values are streamed all the way to the processor, alongside the model weights. But as the batch grows, so does the KV cache. While the goal of batching is to ease memory bandwidth pressure, its gains are partially offset by the KV cache. Because of this, we often cannot scale batch sizes enough to keep the processor fully busy.

[14:00] Now there are further optimizations to ensure memory is used effectively and accommodates for as much data as possible. For instance, the vLLM inference engine came up with paged attention, a mechanism inspired by traditional operating systems to reduce memory fragmentation. But ultimately, memory capacity and bandwidth are still finite and so is the maximum batch size.

[14:25] We are reaching a point where system level engineering optimizations have picked most of the low hanging fruit. It's time to reconsider inference at a higher algorithmic level. The bottleneck there is, in auto regressive models, the fact that every output token requires a full forward pass through a model that has billions or trillions of parameters. But what if we could loosen that constraint?

[14:50] This is the intuition behind the speculative decoding. The decoding steps are delegated to a smaller draft model, which performs forward passes a lot faster. The bigger LLM is repurposed as a verifier for the draft. Given that the draft tokens are readily available, it can now make multiple predictions in a single forward pass similar to the prefill stage we discussed earlier.

[15:15] The longest common prefix between the draft and verifier outputs is committed to the response and the disagreeing tokens are discarded. If we do some quick accounting for this particular example, speculative decoding costs us three light forward passes and a heavy one with an output of two tokens. Regular decoding would've cost us three heavy forward passes with a return of three tokens.

[15:41] So the math works out in favor of speculative decoding only when the draft model is chosen strategically. Too large and it loses its speed advantage over the verifier. Too small and its predictions are always discarded leading to more wasted computations. So it's a tricky balance. What's interesting about speculative decoding is that it makes the large model deal with multiple output tokens in parallel.

[16:07] Pushing this idea to the limit, why not have it deal with all of the output tokens in parallel? If you've been watching my channel for a while, you know where this is going. Diffusion LLMs do exactly that. As you already know, auto-regressive LLMs generate one token at a time until the end of sequence is produced, or a maximum token count is reached. So the number of iterations is dynamically determined by the model for each prompt.

[16:34] Diffusion LLMs are a completely new paradigm. They no longer generate one token at a time, but rather one draft at a time. They start with a fixed context window of complete nonsense and iteratively clean it up into a coherent response. Similar to auto-regressive models, they're still sequential. Each draft needs to wait for the completion of the previous one.

[16:58] However, they perform a fixed number of iterations. This is a hyper parameter that acts as a knob between speed and quality. More iterations take more time, but also improve the response. In a previous video, I covered ways of bringing this number down to tens or hundreds without compromising the final output. For an average LLM response with a few thousand output tokens, a diffusion model will perform fewer iterations than a traditional one.

[17:27] But of course, in case of a yes or no answer, the diffusion chain is longer. An obvious difference between the two paradigms is the amount of work performed per iteration. Diffusion LLMs don't just predict a single token, but update all the tokens in the draft. They still end up producing an end of sequence token somewhere in the context window. But in vanilla implementations, it has no effect until diffusion reaches the final iteration and the programmer throws away the subsequent tokens.

[17:58] So with a single forward pass, that is a single stream of the model weights, they perform more operations than a traditional LLM. That's why diffusion LLMs generally have higher arithmetic intensity and are more likely to be compute bound, falling to the right of the ridge point. How far exactly, directly depends on their context window size. Now if we only judge diffusion LLMs by the roofline model, they look ideal.

[18:25] They fully utilize the available GPU parallelism. But the roofline model is an incomplete picture because it doesn't capture productivity. We could game it by giving the processor busy work like repeatedly multiplying some matrices only to throw them away. In fact, if we look at the runtime measurements, early diffusion models like LLaDA were generally slower than traditional ones. And the larger their context window, the slower they become.

[18:53] So out of the box diffusion LLMs are not necessarily a silver bullet for speed. They just make a different trade off and ask for different kinds of optimizations. We're no longer dealing with the memory bandwidth, but we're asking how can we reduce wasted computations? This recent paper called FOCUS claims that 90% of computations within a refinement step are wasted.

[19:17] The model can only confidently predict about 10% of the tokens. For instance, the model was confident that Harry must be followed by Potter. But the tokens surrounding the conjunction "and" were very ambiguous because a lot of tokens would've made sense here. The FOCUS model attempts to find these high confidence positions ahead of time and only decode those tokens.

[19:40] It's a bit of a greedy strategy that minimizes risk at each step by focusing on low ambiguity positions first, and thus reducing wasted computations. Another source of waste is generating a full context window of thousands of tokens even for prompts that call for a short response. This paper dynamically adjusts the context window across refinements. On the first iteration, they start with a small context window of 64 tokens.

[20:08] Once tokens are decoded, they analyze the probabilities associated with the end of sequence token everywhere in the window. If they're low across the board, they extend the window size for the next iteration. When the end of sequence token starts getting assigned reasonably high probabilities, they lock the response length and continue refining it during the subsequent iterations.

[20:34] While these tricks help, they're not yet mature enough to compete with the years of optimization that have been poured into serving auto-regressive LLMs. To make the best of both worlds, the industry seems to be converging towards block diffusion, a mixture of diffusion and auto regression. Given a long context window, tokens are grouped into blocks. Within each block, tokens are decoded using diffusion, but the blocks themselves are processed sequentially, one after the other.

[21:03] Compared to vanilla diffusion models, this has two major advantages. First of all, decoding can stop early. Once a block produces the end of sequence token, the response can be finalized without diffusing the subsequent blocks. And second, bringing back auto regression allows us to repurpose most optimizations developed for traditional models, including KV caching or speculative decoding.

[21:28] But this time we're less concerned with memory bandwidth since diffusion keeps us in the compute bound region. With block diffusion, we're finally approaching an architecture that neither wastes memory bandwidth, nor leaves the processor idle. We're now starting to see the first inference engines that specifically target diffusion LLMs. On the open source side, there's xDiT, WeDLM, and dInfer, all coming from Chinese labs.

[21:57] On the US side, Inception built their own proprietary inference engine, which enables them to serve diffusion LLMs at more than a thousand tokens per second. They also recently launched Mercury 2, the first diffusion reasoning LLM, which is 10 times faster than other reasoning models on the market. Engineering optimizations and paradigm shifts like diffusion LLMs are two of the most notable ways of dealing with the memory bottleneck and speeding up LLM inference, but there are other techniques as well, including distillation, mixture of experts or quantization on which I have an entire series.

[22:37] For this video and others, you can find my entire reading list on Patreon for free. Thanks for watching, and I'll see you next time.

---

Source: YouTube video by Julia Turc (<https://www.youtube.com/watch?v=BSzhrZOp2x8>). Transcript from youtubegpt (manual). The caption "auto aggressive" is written here as "auto-regressive".
