import { NextResponse } from "next/server";
import { SMART_WALLETS } from "@/lib/data";
export const dynamic="force-dynamic";export const revalidate=0;
export async function GET(){return NextResponse.json({success:true,status:"UNVALIDATED_WATCHLIST",timestamp:Date.now(),count:SMART_WALLETS.length,wallets:SMART_WALLETS,message:"No production smart-wallet cohort is shipped in this package. Populate from validated backend output."});}
